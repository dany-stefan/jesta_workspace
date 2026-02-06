"""
Test README Setup Instructions for Reproducibility
Tests if another person can follow the README setup steps successfully.
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
    END = '\033[0m'

def print_section(title):
    print(f"\n{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 70}{Colors.END}\n")

def print_pass(msg):
    print(f"{Colors.GREEN}✓ PASS{Colors.END} - {msg}")

def print_fail(msg):
    print(f"{Colors.RED}✗ FAIL{Colors.END} - {msg}")

def print_warn(msg):
    print(f"{Colors.YELLOW}⚠ WARN{Colors.END} - {msg}")

def print_info(msg):
    print(f"  {msg}")


class READMESetupTest:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.issues = []
        self.passes = []
        
    def test_prerequisites_mentioned(self):
        """Test if README mentions all prerequisites"""
        print_section("TEST 1: Prerequisites Section")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        required_prereqs = {
            'Python': 'Python 3.9+',
            'pip': 'pip or pip3',
        }
        
        optional_prereqs = {
            'Homebrew': 'brew',
            'macOS': 'macOS',
        }
        
        print_info("Checking if README mentions required prerequisites...")
        all_mentioned = True
        
        for name, keyword in required_prereqs.items():
            if keyword.lower() in readme_content.lower():
                print_pass(f"'{name}' mentioned in README")
            else:
                print_fail(f"'{name}' NOT mentioned in README")
                self.issues.append(f"Missing prerequisite: {name}")
                all_mentioned = False
        
        print_info("\nChecking optional prerequisites...")
        for name, keyword in optional_prereqs.items():
            if keyword.lower() in readme_content.lower():
                print_pass(f"'{name}' mentioned (good for LightGBM setup)")
            else:
                print_warn(f"'{name}' not mentioned (needed for LightGBM)")
        
        return all_mentioned
    
    def test_installation_steps_present(self):
        """Test if README has clear installation steps"""
        print_section("TEST 2: Installation Instructions")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        required_steps = {
            'Navigate to directory': ['cd ', 'dany_stefan_ml_assessment'],
            'Create venv': ['python3 -m venv', 'venv'],
            'Activate venv': ['source', 'activate'],
            'Upgrade pip': ['pip install --upgrade pip'],
            'Install dependencies': ['pip install', 'requirements.txt'],
            'Verify installation': ['import polars', 'import sklearn'],
        }
        
        all_present = True
        
        for step_name, keywords in required_steps.items():
            # Check if all keywords for this step are present
            step_mentioned = all(kw in readme_content for kw in keywords)
            
            if step_mentioned:
                print_pass(f"Step '{step_name}' is documented")
            else:
                print_fail(f"Step '{step_name}' is missing or incomplete")
                self.issues.append(f"Missing installation step: {step_name}")
                all_present = False
        
        return all_present
    
    def test_venv_name_consistency(self):
        """Test if venv name is consistent throughout README"""
        print_section("TEST 3: Virtual Environment Name Consistency")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        # Check what venv names are used
        has_venv = 'venv/bin/activate' in readme_content or 'python3 -m venv venv' in readme_content
        has_dotvenv = '.venv/bin/activate' in readme_content or 'python3 -m venv .venv' in readme_content
        
        # Check which one actually exists
        actual_venv = None
        if (self.project_root.parent / '.venv').exists():
            actual_venv = '.venv'
        elif (self.project_root / 'venv').exists():
            actual_venv = 'venv'
        
        print_info(f"README mentions 'venv': {has_venv}")
        print_info(f"README mentions '.venv': {has_dotvenv}")
        print_info(f"Actual venv in use: {actual_venv}")
        
        if has_venv and has_dotvenv:
            print_fail("README uses BOTH 'venv' and '.venv' - INCONSISTENT!")
            self.issues.append("Inconsistent venv naming in README")
            return False
        elif has_venv and actual_venv == '.venv':
            print_fail("README says 'venv' but actual is '.venv' - MISMATCH!")
            self.issues.append("README venv name doesn't match actual")
            return False
        elif has_dotvenv and actual_venv == 'venv':
            print_fail("README says '.venv' but actual is 'venv' - MISMATCH!")
            self.issues.append("README venv name doesn't match actual")
            return False
        else:
            print_pass("Virtual environment naming is consistent")
            return True
    
    def test_notebook_usage_instructions(self):
        """Test if notebook usage instructions are clear"""
        print_section("TEST 4: Notebook Usage Instructions")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        required_elements = {
            'Activate venv instruction': 'source',
            'Launch Jupyter command': 'jupyter notebook',
            'Notebook filename': 'engineering.ipynb',
            'How to run cells': ['Run All', 'run cells', 'sequentially'],
        }
        
        all_clear = True
        
        for element, keywords in required_elements.items():
            if isinstance(keywords, list):
                found = any(kw.lower() in readme_content.lower() for kw in keywords)
            else:
                found = keywords.lower() in readme_content.lower()
            
            if found:
                print_pass(f"'{element}' is documented")
            else:
                print_fail(f"'{element}' is NOT documented")
                self.issues.append(f"Missing notebook instruction: {element}")
                all_clear = False
        
        # Check if LightGBM cells are mentioned as skippable
        if 'lightgbm' in readme_content.lower() and 'skip' in readme_content.lower():
            print_pass("README mentions LightGBM cells can be skipped")
        else:
            print_warn("README doesn't mention that LightGBM cells are skippable")
            self.issues.append("No guidance on skipping LightGBM cells")
        
        return all_clear
    
    def test_production_code_instructions(self):
        """Test if production_code.py usage instructions are accurate"""
        print_section("TEST 5: production_code.py Instructions")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        # Check what README claims about production_code.py
        claims_working_functions = False
        claims_templates = False
        
        if 'available functions' in readme_content.lower():
            # Check context - is it clear they're templates?
            prod_code_section = readme_content.lower().split('production code')[1] if 'production code' in readme_content.lower() else readme_content.lower()
            
            if 'template' in prod_code_section or 'stub' in prod_code_section or 'todo' in prod_code_section:
                claims_templates = True
                print_pass("README correctly identifies functions as templates/stubs")
            else:
                claims_working_functions = True
                print_fail("README implies functions are working (misleading!)")
                self.issues.append("production_code.py section is misleading")
        
        # Verify actual function implementation
        prod_code_path = self.project_root / "production_code.py"
        if prod_code_path.exists():
            prod_code_content = prod_code_path.read_text()
            
            # Count TODO stubs
            todo_count = prod_code_content.count('# TODO')
            pass_count = prod_code_content.count('pass')
            
            print_info(f"Found {todo_count} TODO comments in production_code.py")
            print_info(f"Found {pass_count} pass statements in production_code.py")
            
            if todo_count > 0 and not claims_templates:
                print_fail("Functions are stubs but README doesn't clarify this")
                self.issues.append("README should clarify production_code.py contains templates")
                return False
            elif todo_count > 0 and claims_templates:
                print_pass("README accurately describes templates")
                return True
            else:
                print_pass("Functions appear to be implemented")
                return True
        else:
            print_fail("production_code.py not found")
            return False
    
    def test_troubleshooting_section(self):
        """Test if troubleshooting section covers common issues"""
        print_section("TEST 6: Troubleshooting Section")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        common_issues = {
            'ModuleNotFoundError': 'Missing dependencies',
            'LightGBM': 'LightGBM/libomp issues',
            'Jupyter kernel': 'Kernel not found',
            'Virtual environment': 'venv activation',
        }
        
        has_troubleshooting = 'troubleshooting' in readme_content.lower()
        
        if not has_troubleshooting:
            print_fail("No Troubleshooting section found in README")
            self.issues.append("Missing Troubleshooting section")
            return False
        
        print_pass("Troubleshooting section exists")
        
        covered_issues = 0
        for issue, description in common_issues.items():
            if issue.lower() in readme_content.lower():
                print_pass(f"Covers '{description}'")
                covered_issues += 1
            else:
                print_warn(f"Doesn't cover '{description}'")
        
        if covered_issues >= 3:
            print_pass(f"Troubleshooting covers {covered_issues}/{len(common_issues)} common issues")
            return True
        else:
            print_warn(f"Troubleshooting only covers {covered_issues}/{len(common_issues)} issues")
            return False
    
    def test_data_file_mentioned(self):
        """Test if data file location is documented"""
        print_section("TEST 7: Data File Documentation")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        data_file_name = 'fashion_sample.csv'
        data_path = 'data/fashion_sample.csv'
        
        if data_file_name in readme_content:
            print_pass(f"Data file '{data_file_name}' is mentioned")
            
            if data_path in readme_content:
                print_pass(f"Full path '{data_path}' is documented")
            else:
                print_warn("Full data path not explicitly shown")
            
            # Check if data file actually exists
            actual_data = self.project_root / 'data' / data_file_name
            if actual_data.exists():
                print_pass(f"Data file exists at {data_path}")
                return True
            else:
                print_fail(f"Data file NOT FOUND at {data_path}")
                self.issues.append("README mentions data file but it doesn't exist")
                return False
        else:
            print_fail(f"Data file '{data_file_name}' not mentioned in README")
            self.issues.append("Data file location not documented")
            return False
    
    def test_requirements_file_instructions(self):
        """Test if requirements.txt is properly documented"""
        print_section("TEST 8: Requirements File Instructions")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        checks = {
            'requirements.txt mentioned': 'requirements.txt' in readme_content,
            'pip install -r command shown': 'pip install -r requirements.txt' in readme_content or 'pip install' in readme_content,
            'requirements.txt exists': (self.project_root / 'requirements.txt').exists(),
        }
        
        all_good = True
        for check, result in checks.items():
            if result:
                print_pass(check)
            else:
                print_fail(check)
                all_good = False
        
        # Check if core dependencies are mentioned
        if 'polars' in readme_content.lower():
            print_pass("Core dependency 'polars' mentioned")
        else:
            print_warn("Core dependency 'polars' not mentioned")
        
        return all_good
    
    def test_quick_start_or_tldr(self):
        """Test if README has quick start for impatient users"""
        print_section("TEST 9: Quick Start / TL;DR Section")
        
        readme_path = self.project_root / "README.md"
        readme_content = readme_path.read_text()
        
        quick_start_keywords = ['quick start', 'tldr', 'tl;dr', 'getting started quickly']
        
        has_quick_start = any(kw in readme_content.lower() for kw in quick_start_keywords)
        
        if has_quick_start:
            print_pass("README has Quick Start section (good UX!)")
            return True
        else:
            print_warn("README lacks Quick Start section")
            print_info("Recommendation: Add Quick Start for reviewers")
            self.issues.append("Consider adding Quick Start section")
            return False
    
    def run_all_tests(self):
        """Run all reproducibility tests"""
        print(f"\n{Colors.BLUE}{'=' * 70}{Colors.END}")
        print(f"{Colors.BLUE}README REPRODUCIBILITY TEST SUITE{Colors.END}")
        print(f"{Colors.BLUE}Testing if another person can follow the README{Colors.END}")
        print(f"{Colors.BLUE}{'=' * 70}{Colors.END}")
        
        tests = [
            self.test_prerequisites_mentioned,
            self.test_installation_steps_present,
            self.test_venv_name_consistency,
            self.test_notebook_usage_instructions,
            self.test_production_code_instructions,
            self.test_troubleshooting_section,
            self.test_data_file_mentioned,
            self.test_requirements_file_instructions,
            self.test_quick_start_or_tldr,
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
        print_section("TEST SUMMARY")
        
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        for test_name, result in results.items():
            if result:
                print_pass(test_name)
            else:
                print_fail(test_name)
        
        print(f"\n{Colors.BLUE}{'=' * 70}{Colors.END}")
        print(f"Tests Passed: {passed}/{total} ({passed/total*100:.0f}%)")
        print(f"{Colors.BLUE}{'=' * 70}{Colors.END}\n")
        
        if self.issues:
            print(f"{Colors.YELLOW}Issues Found:{Colors.END}")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
            print()
        
        if passed == total:
            print(f"{Colors.GREEN}✅ README IS FULLY REPRODUCIBLE{Colors.END}")
            print("Another person should be able to follow the instructions successfully.\n")
            return True
        elif passed >= total * 0.7:
            print(f"{Colors.YELLOW}⚠️ README IS MOSTLY REPRODUCIBLE{Colors.END}")
            print("Most instructions work, but some improvements needed.\n")
            return False
        else:
            print(f"{Colors.RED}❌ README HAS REPRODUCIBILITY ISSUES{Colors.END}")
            print("Significant improvements needed for others to follow.\n")
            return False


if __name__ == "__main__":
    tester = READMESetupTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
