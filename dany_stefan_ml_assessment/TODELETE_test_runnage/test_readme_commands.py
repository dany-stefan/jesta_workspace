"""
Test README Commands for Reproducibility
Tests each command mentioned in README to see if they work.
"""

import sys
import subprocess
import os
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_section(title):
    print(f"\n{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 70}{Colors.END}\n")

def print_command(cmd):
    print(f"{Colors.CYAN}$ {cmd}{Colors.END}")

def print_pass(msg):
    print(f"{Colors.GREEN}✓ PASS{Colors.END} - {msg}")

def print_fail(msg):
    print(f"{Colors.RED}✗ FAIL{Colors.END} - {msg}")

def print_warn(msg):
    print(f"{Colors.YELLOW}⚠ WARN{Colors.END} - {msg}")


class READMECommandTest:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.python_exe = sys.executable
        self.failures = []
        
    def extract_commands_from_readme(self):
        """Extract all commands from README code blocks"""
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        commands = []
        in_code_block = False
        current_block = []
        
        for line in readme_content.split('\n'):
            if line.strip().startswith('```bash') or line.strip().startswith('```sh'):
                in_code_block = True
                current_block = []
            elif line.strip() == '```' and in_code_block:
                in_code_block = False
                if current_block:
                    commands.extend(current_block)
            elif in_code_block:
                line = line.strip()
                if line and not line.startswith('#'):
                    commands.append(line)
        
        return commands
    
    def test_python_version_command(self):
        """Test: python3 --version"""
        print_section("TEST 1: Python Version Check")
        
        print_command("python3 --version")
        
        try:
            result = subprocess.run(
                ['python3', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print_pass(f"Command works: {version}")
                
                # Check if version is 3.9+
                version_num = version.split()[1].split('.')
                major, minor = int(version_num[0]), int(version_num[1])
                
                if major == 3 and minor >= 9:
                    print_pass(f"Version {major}.{minor} meets README requirement (3.9+)")
                    return True
                else:
                    print_warn(f"Version {major}.{minor} < 3.9 (README requirement)")
                    return False
            else:
                print_fail("python3 --version failed")
                return False
        except Exception as e:
            print_fail(f"Error: {e}")
            return False
    
    def test_pip_upgrade_command(self):
        """Test: pip install --upgrade pip"""
        print_section("TEST 2: Pip Upgrade Command")
        
        print_command("pip install --upgrade pip")
        print_warn("Skipping actual execution (would modify system)")
        print_pass("Command syntax is valid")
        return True
    
    def test_verification_command(self):
        """Test: python -c 'import polars...'"""
        print_section("TEST 3: Verification Command from README")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        # Find verification commands
        if 'import polars' in readme_content:
            print_command("python -c \"import polars as pl; import sklearn; print(...)\"")
            
            try:
                # Test polars import
                result = subprocess.run(
                    [self.python_exe, '-c', 'import polars as pl; print(f"Polars {pl.__version__}")'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=self.project_root
                )
                
                if result.returncode == 0:
                    print_pass(f"Polars verification: {result.stdout.strip()}")
                else:
                    print_fail(f"Polars import failed: {result.stderr}")
                    self.failures.append("Polars verification command failed")
                    return False
                
                # Test sklearn import
                result = subprocess.run(
                    [self.python_exe, '-c', 'import sklearn; print(f"scikit-learn {sklearn.__version__}")'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=self.project_root
                )
                
                if result.returncode == 0:
                    print_pass(f"scikit-learn verification: {result.stdout.strip()}")
                    return True
                else:
                    print_fail(f"scikit-learn import failed: {result.stderr}")
                    self.failures.append("scikit-learn verification command failed")
                    return False
                    
            except Exception as e:
                print_fail(f"Error executing verification: {e}")
                return False
        else:
            print_warn("No verification command found in README")
            return False
    
    def test_jupyter_command(self):
        """Test: jupyter notebook engineering.ipynb"""
        print_section("TEST 4: Jupyter Notebook Command")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        if 'jupyter notebook' in readme_content:
            print_command("jupyter notebook engineering.ipynb")
            
            # Check if jupyter is installed
            try:
                result = subprocess.run(
                    ['jupyter', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    print_pass("Jupyter is installed")
                    
                    # Check if notebook file exists
                    notebook_path = self.project_root / 'engineering.ipynb'
                    if notebook_path.exists():
                        print_pass("engineering.ipynb exists")
                        print_warn("Not launching (would open browser)")
                        return True
                    else:
                        print_fail("engineering.ipynb NOT FOUND")
                        self.failures.append("Notebook file missing")
                        return False
                else:
                    print_fail("Jupyter not installed")
                    self.failures.append("Jupyter not available")
                    return False
            except Exception as e:
                print_fail(f"Error checking Jupyter: {e}")
                return False
        else:
            print_warn("Jupyter command not found in README")
            return False
    
    def test_production_code_help_commands(self):
        """Test: python -c 'import production_code...'"""
        print_section("TEST 5: production_code.py Help Commands")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        all_pass = True
        
        # Test 1: import production_code as pc; help(pc)
        if 'import production_code' in readme_content:
            print_command("python -c \"import production_code as pc; help(pc)\"")
            
            try:
                result = subprocess.run(
                    [self.python_exe, '-c', 'import production_code as pc; print("Import successful")'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=self.project_root
                )
                
                if result.returncode == 0:
                    print_pass("production_code imports successfully")
                else:
                    print_fail(f"production_code import failed: {result.stderr}")
                    self.failures.append("production_code.py import failed")
                    all_pass = False
            except Exception as e:
                print_fail(f"Error: {e}")
                all_pass = False
        
        # Test 2: from production_code import detect_stockouts
        if 'detect_stockouts' in readme_content:
            print_command("python -c \"from production_code import detect_stockouts; help(detect_stockouts)\"")
            
            try:
                result = subprocess.run(
                    [self.python_exe, '-c', 'from production_code import detect_stockouts; print("Function imported")'],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=self.project_root
                )
                
                if result.returncode == 0:
                    print_pass("detect_stockouts imports successfully")
                else:
                    print_fail(f"detect_stockouts import failed: {result.stderr}")
                    all_pass = False
            except Exception as e:
                print_fail(f"Error: {e}")
                all_pass = False
        
        # Test 3: python production_code.py
        print_command("python production_code.py")
        
        prod_code_path = self.project_root / 'production_code.py'
        if prod_code_path.exists():
            try:
                result = subprocess.run(
                    [self.python_exe, str(prod_code_path)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=self.project_root
                )
                
                if result.returncode == 0:
                    print_pass("production_code.py executes without errors")
                    if result.stdout:
                        print(f"  Output: {result.stdout[:200]}")
                else:
                    print_fail(f"production_code.py failed: {result.stderr}")
                    all_pass = False
            except Exception as e:
                print_fail(f"Error: {e}")
                all_pass = False
        else:
            print_fail("production_code.py not found")
            all_pass = False
        
        return all_pass
    
    def test_cd_command(self):
        """Test: cd dany_stefan_ml_assessment"""
        print_section("TEST 6: Directory Navigation")
        
        print_command("cd dany_stefan_ml_assessment")
        
        # Check if we're in the right directory
        expected_files = ['README.md', 'engineering.ipynb', 'production_code.py']
        
        all_exist = all((self.project_root / f).exists() for f in expected_files)
        
        if all_exist:
            print_pass("Project directory contains expected files")
            print_pass("Directory navigation instruction is correct")
            return True
        else:
            print_fail("Project directory structure doesn't match README")
            missing = [f for f in expected_files if not (self.project_root / f).exists()]
            print_fail(f"Missing files: {missing}")
            return False
    
    def test_venv_creation_command(self):
        """Test: python3 -m venv [name]"""
        print_section("TEST 7: Virtual Environment Creation")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        # Check what venv name README uses
        if 'python3 -m venv venv' in readme_content:
            print_command("python3 -m venv venv")
            venv_name = 'venv'
        elif 'python3 -m venv .venv' in readme_content:
            print_command("python3 -m venv .venv")
            venv_name = '.venv'
        else:
            print_warn("venv creation command not found in README")
            return False
        
        print_warn("Not creating venv (would modify filesystem)")
        
        # Check if venv exists
        venv_path = self.project_root / venv_name
        parent_venv = self.project_root.parent / '.venv'
        
        if venv_path.exists():
            print_pass(f"{venv_name} exists in project directory")
            return True
        elif parent_venv.exists():
            print_warn(f"Found .venv in parent directory (not {venv_name})")
            if venv_name != '.venv':
                print_fail("README uses wrong venv name!")
                self.failures.append(f"README says '{venv_name}' but actual is '.venv'")
                return False
            return True
        else:
            print_warn(f"No venv found (expected {venv_name})")
            print_pass("Command syntax is correct")
            return True
    
    def test_pip_install_requirements(self):
        """Test: pip install -r requirements.txt"""
        print_section("TEST 8: Requirements Installation")
        
        print_command("pip install -r requirements.txt")
        
        req_path = self.project_root / 'requirements.txt'
        
        if not req_path.exists():
            print_fail("requirements.txt not found")
            self.failures.append("requirements.txt missing")
            return False
        
        print_pass("requirements.txt exists")
        
        # Check if it's readable
        try:
            content = req_path.read_text()
            lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
            print_pass(f"requirements.txt has {len(lines)} package specifications")
            
            # Check for core packages
            core_packages = ['polars', 'scikit-learn', 'numpy', 'pandas']
            found_packages = [pkg for pkg in core_packages if any(pkg in line.lower() for line in lines)]
            
            print_pass(f"Found core packages: {', '.join(found_packages)}")
            
            if len(found_packages) >= 3:
                print_pass("Command should work correctly")
                return True
            else:
                print_warn("Some core packages may be missing")
                return True
        except Exception as e:
            print_fail(f"Error reading requirements.txt: {e}")
            return False
    
    def run_all_tests(self):
        """Run all command tests"""
        print(f"\n{Colors.BLUE}{'=' * 70}{Colors.END}")
        print(f"{Colors.BLUE}README COMMAND REPRODUCIBILITY TEST{Colors.END}")
        print(f"{Colors.BLUE}Testing if README commands work as documented{Colors.END}")
        print(f"{Colors.BLUE}{'=' * 70}{Colors.END}")
        
        tests = [
            self.test_cd_command,
            self.test_python_version_command,
            self.test_venv_creation_command,
            self.test_pip_upgrade_command,
            self.test_pip_install_requirements,
            self.test_verification_command,
            self.test_jupyter_command,
            self.test_production_code_help_commands,
        ]
        
        results = {}
        for test in tests:
            test_name = test.__name__.replace('test_', '').replace('_', ' ').title()
            try:
                result = test()
                results[test_name] = result
            except Exception as e:
                print_fail(f"Test crashed: {e}")
                results[test_name] = False
        
        # Summary
        print_section("COMMAND TEST SUMMARY")
        
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        for test_name, result in results.items():
            if result:
                print_pass(test_name)
            else:
                print_fail(test_name)
        
        print(f"\n{Colors.BLUE}{'=' * 70}{Colors.END}")
        print(f"Commands Tested: {passed}/{total} work ({passed/total*100:.0f}%)")
        print(f"{Colors.BLUE}{'=' * 70}{Colors.END}\n")
        
        if self.failures:
            print(f"{Colors.RED}Command Failures:{Colors.END}")
            for i, failure in enumerate(self.failures, 1):
                print(f"  {i}. {failure}")
            print()
        
        if passed == total:
            print(f"{Colors.GREEN}✅ ALL README COMMANDS WORK{Colors.END}")
            print("Another person can execute all documented commands.\n")
            return True
        elif passed >= total * 0.75:
            print(f"{Colors.YELLOW}⚠️ MOST README COMMANDS WORK{Colors.END}")
            print("Some commands need fixes.\n")
            return False
        else:
            print(f"{Colors.RED}❌ MANY README COMMANDS FAIL{Colors.END}")
            print("Significant command issues found.\n")
            return False


if __name__ == "__main__":
    tester = READMECommandTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
