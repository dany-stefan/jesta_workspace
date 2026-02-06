"""
Test README End-to-End Workflow
Simulates a new user following README from start to finish.
"""

import sys
import json
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(num, title):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}STEP {num}: {title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_pass(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_fail(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_warn(msg):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_info(msg):
    print(f"  {msg}")


class WorkflowSimulation:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.readme_path = self.project_root / "README.md"
        self.blockers = []
        self.warnings = []
        self.success_steps = []
        
    def read_readme_section(self, section_name):
        """Extract a section from README"""
        if not self.readme_path.exists():
            return None
        
        content = self.readme_path.read_text()
        return content
    
    def step_1_find_readme(self):
        """User opens project folder and looks for README"""
        print_step(1, "Find and Open README")
        
        print_info("New user: 'Let me find the README to get started...'")
        
        if self.readme_path.exists():
            print_pass("README.md found in project root")
            
            # Check README size
            size = self.readme_path.stat().st_size
            print_pass(f"README is {size:,} bytes ({size/1024:.1f} KB)")
            
            # Check if it has content
            content = self.readme_path.read_text()
            lines = len(content.split('\n'))
            
            if lines > 50:
                print_pass(f"README has {lines} lines (detailed documentation)")
            else:
                print_warn(f"README only has {lines} lines (may lack detail)")
            
            self.success_steps.append("Found README")
            return True
        else:
            print_fail("README.md NOT FOUND")
            print_fail("BLOCKER: User cannot proceed without documentation")
            self.blockers.append("No README.md file")
            return False
    
    def step_2_understand_prerequisites(self):
        """User reads prerequisites section"""
        print_step(2, "Understand Prerequisites")
        
        print_info("New user: 'What do I need installed before starting?'")
        
        content = self.read_readme_section("Prerequisites")
        
        if not content:
            print_fail("Could not read README")
            return False
        
        # Check for prerequisites section
        has_prereq_section = 'prerequisite' in content.lower() or 'requirement' in content.lower()
        
        if not has_prereq_section:
            print_fail("No Prerequisites section found")
            print_warn("User doesn't know what to install first")
            self.warnings.append("Missing Prerequisites section")
            return False
        
        print_pass("Prerequisites section exists")
        
        # Check for key prerequisites
        prereqs = {
            'Python': 'python' in content.lower() and '3.9' in content,
            'pip': 'pip' in content.lower(),
            'Homebrew (macOS)': 'brew' in content.lower() or 'homebrew' in content.lower(),
        }
        
        for prereq, found in prereqs.items():
            if found:
                print_pass(f"Mentions: {prereq}")
            else:
                if 'macOS' not in prereq:
                    print_warn(f"Doesn't mention: {prereq}")
        
        self.success_steps.append("Understood prerequisites")
        return True
    
    def step_3_follow_installation(self):
        """User follows installation instructions"""
        print_step(3, "Follow Installation Instructions")
        
        print_info("New user: 'Let me follow the installation steps...'")
        
        content = self.read_readme_section("Installation")
        
        # Check for installation section
        has_install = 'installation' in content.lower() or 'setup' in content.lower()
        
        if not has_install:
            print_fail("No Installation section found")
            self.blockers.append("Missing installation instructions")
            return False
        
        print_pass("Installation section exists")
        
        # Check for numbered/clear steps
        install_section = content[content.lower().find('installation'):content.lower().find('installation') + 2000]
        
        steps_found = []
        
        # Check for venv creation
        if 'venv' in install_section:
            print_pass("Step: Create virtual environment documented")
            steps_found.append("venv")
        else:
            print_fail("Missing: Virtual environment creation")
            self.blockers.append("No venv creation step")
        
        # Check for pip install
        if 'pip install' in install_section:
            print_pass("Step: Install dependencies documented")
            steps_found.append("pip install")
        else:
            print_fail("Missing: Dependency installation")
            self.blockers.append("No pip install step")
        
        # Check for verification
        if 'import polars' in content or 'verify' in install_section.lower():
            print_pass("Step: Verification command provided")
            steps_found.append("verify")
        else:
            print_warn("Missing: Installation verification step")
            self.warnings.append("No verification command")
        
        if len(steps_found) >= 2:
            self.success_steps.append("Completed installation")
            return True
        else:
            print_fail(f"Incomplete installation steps (found {len(steps_found)}/3)")
            return False
    
    def step_4_run_notebook(self):
        """User tries to run the notebook"""
        print_step(4, "Run Jupyter Notebook")
        
        print_info("New user: 'How do I run the analysis notebook?'")
        
        content = self.read_readme_section("notebook")
        
        # Check for notebook instructions
        has_notebook_section = 'jupyter' in content.lower() and 'notebook' in content.lower()
        
        if not has_notebook_section:
            print_fail("No Jupyter notebook instructions found")
            self.warnings.append("Unclear how to run notebook")
            return False
        
        print_pass("Jupyter notebook section exists")
        
        # Check for activation reminder
        if 'activate' in content:
            print_pass("Reminds user to activate venv")
        else:
            print_warn("Doesn't remind to activate venv (user may forget)")
            self.warnings.append("No venv activation reminder")
        
        # Check for jupyter command
        if 'jupyter notebook' in content:
            print_pass("Jupyter launch command provided")
        else:
            print_fail("Missing jupyter launch command")
            return False
        
        # Check if notebook file exists
        notebook_path = self.project_root / 'engineering.ipynb'
        if notebook_path.exists():
            print_pass("engineering.ipynb exists in project")
            
            # Check notebook structure
            try:
                with open(notebook_path) as f:
                    nb = json.load(f)
                
                cells = len(nb.get('cells', []))
                code_cells = sum(1 for c in nb['cells'] if c.get('cell_type') == 'code')
                
                print_pass(f"Notebook has {cells} cells ({code_cells} code cells)")
                
                # Check for errors in outputs
                error_cells = []
                for i, cell in enumerate(nb['cells']):
                    if cell.get('cell_type') == 'code':
                        outputs = cell.get('outputs', [])
                        for output in outputs:
                            if output.get('output_type') == 'error':
                                error_cells.append(i + 1)
                
                if error_cells:
                    print_warn(f"{len(error_cells)} cells have error outputs")
                    
                    # Check if README mentions skipping errors
                    if 'skip' in content.lower() and ('lightgbm' in content.lower() or 'cell' in content.lower()):
                        print_pass("README mentions skipping problematic cells")
                    else:
                        print_warn("README doesn't mention how to handle cell errors")
                        self.warnings.append("No guidance on error cells")
                else:
                    print_pass("No error outputs in notebook")
                
            except Exception as e:
                print_warn(f"Could not analyze notebook: {e}")
        else:
            print_fail("engineering.ipynb NOT FOUND")
            self.blockers.append("Notebook file missing")
            return False
        
        self.success_steps.append("Ran notebook")
        return True
    
    def step_5_explore_production_code(self):
        """User tries to use production_code.py"""
        print_step(5, "Explore Production Code")
        
        print_info("New user: 'Let me check out the production code...'")
        
        content = self.read_readme_section("production")
        
        # Check for production code section
        has_prod_section = 'production' in content.lower() and 'code' in content.lower()
        
        if not has_prod_section:
            print_warn("No production code section in README")
            return True  # Not critical
        
        print_pass("Production code section exists")
        
        # Check if it's clear about implementation status
        prod_section = content[content.lower().find('production'):content.lower().find('production') + 1500]
        
        if 'template' in prod_section.lower() or 'stub' in prod_section.lower():
            print_pass("README clearly states functions are templates/stubs")
        elif 'available functions' in prod_section.lower():
            # Check if functions are actually implemented
            prod_code_path = self.project_root / 'production_code.py'
            if prod_code_path.exists():
                prod_code = prod_code_path.read_text()
                if '# TODO' in prod_code:
                    print_fail("README says 'available functions' but they're TODO stubs")
                    print_fail("MISLEADING: User expects working code")
                    self.warnings.append("production_code.py section is misleading")
                else:
                    print_pass("Functions appear to be implemented")
        
        # Check if file exists
        prod_code_path = self.project_root / 'production_code.py'
        if prod_code_path.exists():
            print_pass("production_code.py exists")
            
            # Try to import
            try:
                import production_code
                print_pass("production_code.py can be imported")
            except Exception as e:
                print_fail(f"Cannot import production_code.py: {e}")
                return False
        else:
            print_fail("production_code.py NOT FOUND")
            self.blockers.append("production_code.py missing")
            return False
        
        self.success_steps.append("Explored production code")
        return True
    
    def step_6_check_data(self):
        """User looks for data files"""
        print_step(6, "Locate Data Files")
        
        print_info("New user: 'Where is the data I need to run this?'")
        
        content = self.read_readme_section("data")
        
        # Check if data location is mentioned
        if 'fashion_sample.csv' in content:
            print_pass("Data file name mentioned in README")
        else:
            print_warn("Data file name not mentioned")
        
        if 'data/' in content:
            print_pass("Data directory path mentioned")
        else:
            print_warn("Data directory path not clear")
        
        # Check if data exists
        data_file = self.project_root / 'data' / 'fashion_sample.csv'
        if data_file.exists():
            print_pass("data/fashion_sample.csv exists")
            
            size = data_file.stat().st_size
            print_pass(f"Data file is {size:,} bytes ({size/1024:.1f} KB)")
            
            # Try to read first line
            try:
                with open(data_file) as f:
                    header = f.readline().strip()
                print_pass(f"Header: {header[:60]}...")
            except Exception as e:
                print_warn(f"Could not read data file: {e}")
        else:
            print_fail("data/fashion_sample.csv NOT FOUND")
            self.blockers.append("Data file missing")
            return False
        
        self.success_steps.append("Found data")
        return True
    
    def step_7_troubleshooting(self):
        """User encounters an error and checks troubleshooting"""
        print_step(7, "Handle Errors (Troubleshooting)")
        
        print_info("New user: 'I got an error - let me check troubleshooting...'")
        
        content = self.read_readme_section("troubleshoot")
        
        # Check for troubleshooting section
        if 'troubleshoot' in content.lower():
            print_pass("Troubleshooting section exists")
        else:
            print_warn("No Troubleshooting section")
            self.warnings.append("Missing troubleshooting section")
            return False
        
        # Check for common issues
        common_issues = {
            'ModuleNotFoundError': 'Missing package errors',
            'LightGBM': 'LightGBM/libomp issues',
            'kernel': 'Jupyter kernel issues',
            'activate': 'Virtual environment issues',
        }
        
        found_solutions = 0
        for issue, description in common_issues.items():
            if issue.lower() in content.lower():
                print_pass(f"Covers: {description}")
                found_solutions += 1
            else:
                print_warn(f"Doesn't cover: {description}")
        
        if found_solutions >= 2:
            print_pass(f"Troubleshooting covers {found_solutions}/{len(common_issues)} common issues")
            self.success_steps.append("Can troubleshoot errors")
            return True
        else:
            print_warn("Limited troubleshooting coverage")
            return False
    
    def simulate_workflow(self):
        """Simulate entire user workflow"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}README WORKFLOW SIMULATION{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}Simulating new user following README from scratch{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        
        workflow_steps = [
            self.step_1_find_readme,
            self.step_2_understand_prerequisites,
            self.step_3_follow_installation,
            self.step_4_run_notebook,
            self.step_5_explore_production_code,
            self.step_6_check_data,
            self.step_7_troubleshooting,
        ]
        
        for step_func in workflow_steps:
            success = step_func()
            
            if not success and self.blockers:
                print(f"\n{Colors.RED}🛑 BLOCKER ENCOUNTERED{Colors.END}")
                print(f"User cannot proceed: {self.blockers[-1]}")
                break
        
        # Final Report
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}WORKFLOW SIMULATION REPORT{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        print(f"{Colors.GREEN}✓ Success Steps:{Colors.END}")
        for i, step in enumerate(self.success_steps, 1):
            print(f"  {i}. {step}")
        
        if self.warnings:
            print(f"\n{Colors.YELLOW}⚠ Warnings:{Colors.END}")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if self.blockers:
            print(f"\n{Colors.RED}🛑 Blockers:{Colors.END}")
            for i, blocker in enumerate(self.blockers, 1):
                print(f"  {i}. {blocker}")
        
        print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
        
        total_steps = len(workflow_steps)
        completed_steps = len(self.success_steps)
        
        print(f"Workflow Progress: {completed_steps}/{total_steps} steps ({completed_steps/total_steps*100:.0f}%)")
        
        if self.blockers:
            print(f"\n{Colors.RED}❌ USER WOULD BE BLOCKED{Colors.END}")
            print("Critical issues prevent completion of workflow.\n")
            return False
        elif len(self.warnings) > 3:
            print(f"\n{Colors.YELLOW}⚠️ USER WOULD STRUGGLE{Colors.END}")
            print("Multiple issues would cause confusion and delays.\n")
            return False
        elif completed_steps == total_steps:
            print(f"\n{Colors.GREEN}✅ USER WOULD SUCCEED{Colors.END}")
            print("Workflow is smooth and reproducible!\n")
            return True
        else:
            print(f"\n{Colors.YELLOW}⚠️ USER MIGHT SUCCEED WITH EFFORT{Colors.END}")
            print("Some steps unclear but workaround possible.\n")
            return False


if __name__ == "__main__":
    simulator = WorkflowSimulation()
    success = simulator.simulate_workflow()
    sys.exit(0 if success else 1)
