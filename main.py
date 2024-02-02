import subprocess
import json
from pprint import pprint
from typing import Dict, Tuple, List


class PackageManager:
    @staticmethod
    def get_installed_packages() -> Dict[str, Dict[str, str]]:
        pacman_packages = subprocess.run(['pacman', '-Qe'], capture_output=True, text=True).stdout.split('\n')
        aur_packages = subprocess.run(['pacman', '-Qem'], capture_output=True, text=True).stdout.split('\n')

        pacman_dict = PackageManager._parse_package_list(pacman_packages)
        aur_dict = PackageManager._parse_package_list(aur_packages)

        return {
            "pacman": pacman_dict,
            "aur": aur_dict
        }

    @staticmethod
    def _parse_package_list(package_list: List[str]) -> Dict[str, str]:
        package_dict = {}
        for package in package_list:
            if package:
                name, version = package.split(' ')
                package_dict[name] = version
        return package_dict

    @staticmethod
    def filter_aur_packages(aur_packages: Dict[str, str]) -> Dict[str, str]:
        official_packages = PackageManager._get_official_packages()
        return {
            name: version
            for name, version in aur_packages.items()
            if name not in official_packages
        }

    @staticmethod
    def filter_pacman_packages(pacman_packages: Dict[str, str], aur_packages: Dict[str, str]) -> Dict[str, str]:
        return {
            key: pacman_packages[key]
            for key in pacman_packages
            if key not in aur_packages
        }

    @staticmethod
    def _get_official_packages() -> List[str]:
        official_packages = subprocess.run(['pacman', '-Slq'], capture_output=True, text=True).stdout.split('\n')
        return official_packages


class PackageComparator:
    @staticmethod
    def compare_installed_packages(
            old_dict: Dict[str, Dict[str, str]],
            new_dict: Dict[str, Dict[str, str]]
    ) -> Tuple[Dict[str, str], Dict[str, str]]:
        added_packages = {
            **PackageComparator._find_added_packages(old_dict, new_dict, "pacman"),
            **PackageComparator._find_added_packages(old_dict, new_dict, "aur")
        }
        removed_packages = {
            **PackageComparator._find_removed_packages(old_dict, new_dict, "pacman"),
            **PackageComparator._find_removed_packages(old_dict, new_dict, "aur"),
        }
        return added_packages, removed_packages

    @staticmethod
    def _find_added_packages(
            old_dict: Dict[str, Dict[str, str]],
            new_dict: Dict[str, Dict[str, str]],
            package_type: str
    ) -> Dict[str, str]:
        return {
            name: version
            for name, version in new_dict[package_type].items()
            if name not in old_dict[package_type]
        }

    @staticmethod
    def _find_removed_packages(
            old_dict: Dict[str, Dict[str, str]],
            new_dict: Dict[str, Dict[str, str]],
            package_type: str
    ) -> Dict[str, str]:
        return {
            name: version
            for name, version in old_dict[package_type].items()
            if name not in new_dict[package_type]
        }


def load_previous_packages(file_path: str) -> Dict[str, Dict[str, str]]:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_packages_to_json(packages: Dict[str, Dict[str, str]], file_path: str) -> None:
    with open(file_path, 'w') as file:
        json.dump(packages, file, indent=4)


def main() -> None:
    previous = load_previous_packages('previous.json')
    current = PackageManager.get_installed_packages()

    filtered_aur_packages = PackageManager.filter_aur_packages(current["aur"])
    filtered_pacman_packages = PackageManager.filter_pacman_packages(current["pacman"], filtered_aur_packages)
    current_packages = {
        "pacman": filtered_pacman_packages,
        "aur": filtered_aur_packages
    }

    added, removed = PackageComparator.compare_installed_packages(previous, current_packages)
    save_packages_to_json(current_packages, 'current.json')

    print("Newly installed packages:")
    pprint(added)
    print("\nRemoved packages:")
    pprint(removed)


if __name__ == "__main__":
    main()
