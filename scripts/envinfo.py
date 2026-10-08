import argparse
import importlib.metadata
import importlib.util
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import url2pathname


def collect_env_info() -> dict[str, Any]:
    """Collects general interpreter and environment information."""
    env_venv = os.environ.get("VIRTUAL_ENV")
    env_pythonpath = os.environ.get("PYTHONPATH")
    is_venv = sys.prefix != sys.base_prefix

    venv_mismatch = False
    if env_venv and Path(env_venv).resolve() != Path(sys.prefix).resolve():
        venv_mismatch = True

    return {
        "executable": sys.executable,
        "version": sys.version,
        "implementation": platform.python_implementation(),
        "platform": sys.platform,
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
        "virtual_env": env_venv,
        "pythonpath": env_pythonpath,
        "flags_isolated": sys.flags.isolated,
        "flags_safe_path": sys.flags.safe_path,
        "is_venv": is_venv,
        "venv_mismatch": venv_mismatch,
        "sys_path": sys.path,
    }


def analyze_module(module_name: str) -> dict[str, Any]:
    """Analyzes a module's source location, distribution mapping, and checks for shadowing."""
    result = {
        "module_name": module_name,
        "is_stdlib": module_name in sys.stdlib_module_names,
        "spec_origin": None,
        "spec_origin_path": None,
        "is_namespace": False,
        "distributions": [],
        "shadowing_detected": False,
        "details": [],
    }

    # 1. Check module source via find_spec
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            if spec.origin is None and spec.submodule_search_locations:
                result["is_namespace"] = True
                locations = list(spec.submodule_search_locations)
                result["spec_origin"] = f"Namespace package at {locations}"
                if locations:
                    result["spec_origin_path"] = Path(locations[0]).resolve()
            else:
                result["spec_origin"] = spec.origin
                if spec.origin:
                    result["spec_origin_path"] = Path(spec.origin).resolve()
    except (ImportError, ValueError) as e:
        result["details"].append(f"Error while searching for specification: {e}")

    if result["is_stdlib"]:
        return result

    # 2. Map module name to distributions
    dist_names = []
    try:
        dist_map = importlib.metadata.packages_distributions()
        dist_names = dist_map.get(module_name, [])
    except (KeyError, TypeError):
        pass

    # Fallback: try direct distribution lookup with normalized name
    if not dist_names:
        normalized_name = module_name.replace("_", "-")
        try:
            # Verify if it exists
            importlib.metadata.distribution(normalized_name)
            dist_names = [normalized_name]
        except importlib.metadata.PackageNotFoundError:
            pass

    if not dist_names and not result["spec_origin"]:
        return result

    # 3. Analyze distributions and check ownership/shadowing
    for dist_name in dist_names:
        try:
            dist = importlib.metadata.distribution(dist_name)
            installed_at = Path(dist.locate_file("")).resolve()

            # Check for editable install via direct_url.json
            editable_source_root = None
            try:
                raw = dist.read_text("direct_url.json")
                if raw:
                    info = json.loads(raw)
                    if info.get("dir_info", {}).get("editable"):
                        parsed_url = urlparse(info.get("url", ""))
                        editable_source_root = Path(
                            url2pathname(parsed_url.path)
                        ).resolve()
            except (FileNotFoundError, json.JSONDecodeError, OSError):
                pass

            dist_info = {
                "name": dist_name,
                "version": dist.version,
                "installed_at": installed_at,
                "editable_source_root": editable_source_root,
                "owned": False,
            }

            # Check ownership / shadowing
            spec_path = result["spec_origin_path"]
            if spec_path:
                if editable_source_root:
                    # For editable installs, check if spec path is relative to the source root
                    try:
                        if spec_path.is_relative_to(editable_source_root):
                            dist_info["owned"] = True
                        else:
                            result["shadowing_detected"] = True
                    except ValueError:
                        result["shadowing_detected"] = True
                else:
                    # For standard installs, check against RECORD files (dist.files)
                    owned = False
                    if dist.files:
                        for f in dist.files:
                            try:
                                if Path(dist.locate_file(f)).resolve() == spec_path:
                                    owned = True
                                    break
                            except OSError:
                                continue
                    dist_info["owned"] = owned
                    if not owned:
                        result["shadowing_detected"] = True

            result["distributions"].append(dist_info)
        except importlib.metadata.PackageNotFoundError as e:
            result["details"].append(
                f"Could not retrieve metadata for distribution '{dist_name}': {e}"
            )

    return result


def print_report(env_info: dict[str, Any], module_analysis: dict[str, Any]) -> None:
    """Prints the formatted diagnostic report."""
    print("=" * 65)
    print("1. INTERPRETER & VERSION")
    print("=" * 65)
    print(f"sys.executable:      {env_info['executable']}")
    print(f"sys.version:         {env_info['version']}")
    print(f"Python implement.:   {env_info['implementation']}")
    print(f"sys.platform:        {env_info['platform']}")

    print("\n" + "=" * 65)
    print("2. ENVIRONMENT & VENV ISOLATION")
    print("=" * 65)
    print(f"sys.prefix:          {env_info['prefix']}")
    print(f"sys.base_prefix:     {env_info['base_prefix']}")
    print(
        "VIRTUAL_ENV env var:"
        f" {env_info['virtual_env'] if env_info['virtual_env'] else '<not set>'}"
    )
    print(
        "PYTHONPATH env var: "
        f" {env_info['pythonpath'] if env_info['pythonpath'] else '<not set>'}"
    )
    print(f"sys.flags.isolated:  {env_info['flags_isolated']}")
    print(f"sys.flags.safe_path: {env_info['flags_safe_path']}")
    print(f"Venv verdict:        {'YES' if env_info['is_venv'] else 'NO'}")

    if env_info["venv_mismatch"]:
        print(
            "WARNING:             VIRTUAL_ENV environment variable does not match"
            " sys.prefix!"
        )

    print("\n" + "=" * 65)
    print("3. SYS.PATH (SEARCH ORDER)")
    print("=" * 65)
    for idx, path_entry in enumerate(env_info["sys_path"]):
        print(f"  [{idx}] {path_entry}")

    print("\n" + "=" * 65)
    print(f"4. MODULE ANALYSIS & SHADOWING DETECTION: {module_analysis['module_name']}")
    print("=" * 65)

    if module_analysis["is_stdlib"]:
        print("Module source:       Standard Library module")
        print("Shadowing check:     OK (Python Standard Library)")
        print("=" * 65)
        return

    if not module_analysis["spec_origin"]:
        print(
            f"Module source:       Module '{module_analysis['module_name']}' was"
            " not found in sys.path."
        )
    else:
        print(f"Module source:       {module_analysis['spec_origin']}")

    if not module_analysis["distributions"]:
        print(
            "Distribution mapping: No matching installed distribution found via"
            " metadata."
        )
    else:
        for dist in module_analysis["distributions"]:
            print(f"Installed dist:      {dist['name']} (version {dist['version']})")
            print(f"                     Location: {dist['installed_at']}")
            if dist["editable_source_root"]:
                print(f"Editable source:     {dist['editable_source_root']}")

            if module_analysis["spec_origin_path"]:
                if dist["owned"]:
                    print(
                        "Shadowing check:     OK (module belongs to the installed"
                        " distribution)"
                    )
                else:
                    print(
                        "WARNING:             Module would be imported from"
                        " OUTSIDE the installed distribution -> SHADOWING DETECTED!"
                    )

    for detail in module_analysis["details"]:
        print(f"Detail:              {detail}")

    print("=" * 65)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Advanced diagnostic tool for Python environments, path isolation,"
            " and module shadowing."
        )
    )
    parser.add_argument(
        "module_name",
        help=(
            "Name of the module to analyze (e.g., pydantic, yaml, sklearn,"
            " de_python_libs)"
        ),
    )
    args = parser.parse_args()

    env_info = collect_env_info()
    module_analysis = analyze_module(args.module_name)
    print_report(env_info, module_analysis)

    # Exit with non-zero status if shadowing is detected (useful for CI/CD)
    if module_analysis.get("shadowing_detected", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
