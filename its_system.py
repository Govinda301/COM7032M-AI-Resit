import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import random
import json
from datetime import datetime

class IntelligentTutoringSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Tutoring System - Geometry & Algebra")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Student progress tracking
        self.student_progress = {
            'geometry': {'correct': 0, 'total': 0, 'topics_covered': set()},
            'algebra': {'correct': 0, 'total': 0, 'topics_covered': set()},
            'difficulty_level': 'beginner'  # beginner, intermediate, advanced
        }
        
        # Current problem data
        self.current_problem = None
        self.current_answer = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="<“ Intelligent Tutoring System", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.setup_geometry_tab()
        self.setup_algebra_tab()
        self.setup_progress_tab()
        self.setup_help_tab()
        
    def setup_geometry_tab(self):
        # Geometry tab
        self.geometry_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.geometry_frame, text="=Ð Geometry - Area Calculations")
        
        # Shape selection
        shape_frame = tk.LabelFrame(self.geometry_frame, text="Select Shape", 
                                   font=('Arial', 12, 'bold'), padx=10, pady=10)
        shape_frame.pack(fill='x', padx=10, pady=5)
        
        shapes = [
            ("Triangle", "triangle"),
            ("Square", "square"), 
            ("Rectangle", "rectangle"),
            ("Circle", "circle")
        ]
        
        self.shape_var = tk.StringVar(value="triangle")
        for text, value in shapes:
            tk.Radiobutton(shape_frame, text=text, variable=self.shape_var, 
                          value=value, font=('Arial', 11),
                          command=self.update_geometry_display).pack(side='left', padx=20)
        
        # Problem display
        self.geometry_problem_frame = tk.LabelFrame(self.geometry_frame, text="Problem", 
                                                   font=('Arial', 12, 'bold'), padx=10, pady=10)
        self.geometry_problem_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.geometry_problem_text = scrolledtext.ScrolledText(
            self.geometry_problem_frame, height=8, font=('Arial', 11), 
            wrap=tk.WORD, state='disabled')
        self.geometry_problem_text.pack(fill='both', expand=True, pady=5)
        
        # Input and controls
        input_frame = tk.Frame(self.geometry_frame)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(input_frame, text="Your Answer:", font=('Arial', 11, 'bold')).pack(side='left')
        self.geometry_answer_entry = tk.Entry(input_frame, font=('Arial', 11), width=15)
        self.geometry_answer_entry.pack(side='left', padx=(10, 5))
        
        tk.Button(input_frame, text="Submit Answer", command=self.check_geometry_answer,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(input_frame, text="New Problem", command=self.generate_geometry_problem,
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(input_frame, text="Show Hint", command=self.show_geometry_hint,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Feedback area
        self.geometry_feedback = tk.Text(self.geometry_frame, height=4, font=('Arial', 10),
                                        bg='#ecf0f1', state='disabled')
        self.geometry_feedback.pack(fill='x', padx=10, pady=5)
        
        # Generate initial problem
        self.generate_geometry_problem()
        
    def setup_algebra_tab(self):
        # Algebra tab
        self.algebra_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.algebra_frame, text=" Algebra - Quadratic Equations")
        
        # Difficulty selection
        diff_frame = tk.LabelFrame(self.algebra_frame, text="Difficulty Level", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        diff_frame.pack(fill='x', padx=10, pady=5)
        
        difficulties = [("Beginner", "beginner"), ("Intermediate", "intermediate"), ("Advanced", "advanced")]
        self.difficulty_var = tk.StringVar(value="beginner")
        
        for text, value in difficulties:
            tk.Radiobutton(diff_frame, text=text, variable=self.difficulty_var, 
                          value=value, font=('Arial', 11)).pack(side='left', padx=20)
        
        # Problem display
        self.algebra_problem_frame = tk.LabelFrame(self.algebra_frame, text="Quadratic Equation Problem", 
                                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        self.algebra_problem_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.algebra_problem_text = scrolledtext.ScrolledText(
            self.algebra_problem_frame, height=8, font=('Arial', 11), 
            wrap=tk.WORD, state='disabled')
        self.algebra_problem_text.pack(fill='both', expand=True, pady=5)
        
        # Input and controls
        input_frame = tk.Frame(self.algebra_frame)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(input_frame, text="Solutions (comma-separated):", font=('Arial', 11, 'bold')).pack(side='left')
        self.algebra_answer_entry = tk.Entry(input_frame, font=('Arial', 11), width=20)
        self.algebra_answer_entry.pack(side='left', padx=(10, 5))
        
        tk.Button(input_frame, text="Submit Answer", command=self.check_algebra_answer,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(input_frame, text="New Problem", command=self.generate_algebra_problem,
                 bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(input_frame, text="Show Steps", command=self.show_algebra_steps,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Feedback area
        self.algebra_feedback = tk.Text(self.algebra_frame, height=4, font=('Arial', 10),
                                       bg='#ecf0f1', state='disabled')
        self.algebra_feedback.pack(fill='x', padx=10, pady=5)
        
        # Generate initial problem
        self.generate_algebra_problem()
        
    def setup_progress_tab(self):
        # Progress tracking tab
        self.progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.progress_frame, text=" Progress Tracking")
        
        # Progress display
        progress_info = tk.LabelFrame(self.progress_frame, text="Your Learning Progress", 
                                     font=('Arial', 12, 'bold'), padx=10, pady=10)
        progress_info.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.progress_text = scrolledtext.ScrolledText(progress_info, font=('Arial', 11), 
                                                      state='disabled')
        self.progress_text.pack(fill='both', expand=True, pady=5)
        
        # Update button
        tk.Button(self.progress_frame, text="Update Progress", command=self.update_progress_display,
                 bg='#9b59b6', fg='white', font=('Arial', 11, 'bold')).pack(pady=10)
        
        self.update_progress_display()
        
    def setup_help_tab(self):
        # Help tab
        self.help_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.help_frame, text=" Help & Formulas")
        
        help_content = """
 GEOMETRY FORMULAS:

Triangle Area:
" Formula: A = (1/2) × base × height
" Example: If base = 6 and height = 4, then A = (1/2) × 6 × 4 = 12

Square Area:
" Formula: A = side²
" Example: If side = 5, then A = 5² = 25

Rectangle Area:
" Formula: A = length × width
" Example: If length = 8 and width = 3, then A = 8 × 3 = 24

Circle Area:
" Formula: A = À × radius²
" Example: If radius = 3, then A = À × 3² = À × 9 H 28.27

 QUADRATIC EQUATIONS:

Standard Form: ax² + bx + c = 0

Quadratic Formula:
x = (-b ± (b² - 4ac)) / (2a)

Methods to Solve:
1. Factoring (when possible)
2. Quadratic Formula (always works)
3. Completing the Square

Example: x² - 5x + 6 = 0
" Factor: (x - 2)(x - 3) = 0
" Solutions: x = 2 or x = 3

 TIPS FOR SUCCESS:
" Read problems carefully
" Show your work step by step
" Check your answers by substituting back
" Practice regularly to improve
" Use hints when you're stuck
        """
        
        help_text = scrolledtext.ScrolledText(self.help_frame, font=('Arial', 11), wrap=tk.WORD)
        help_text.pack(fill='both', expand=True, padx=10, pady=10)
        help_text.insert('1.0', help_content)
        help_text.config(state='disabled')
        
    def update_geometry_display(self):
        self.generate_geometry_problem()
        
    def generate_geometry_problem(self):
        shape = self.shape_var.get()
        difficulty = self.student_progress['difficulty_level']
        
        if shape == "triangle":
            self.generate_triangle_problem(difficulty)
        elif shape == "square":
            self.generate_square_problem(difficulty)
        elif shape == "rectangle":
            self.generate_rectangle_problem(difficulty)
        elif shape == "circle":
            self.generate_circle_problem(difficulty)
            
        self.geometry_answer_entry.delete(0, tk.END)
        self.update_text_widget(self.geometry_feedback, "")
        
    def generate_triangle_problem(self, difficulty):
        if difficulty == "beginner":
            base = random.randint(3, 10)
            height = random.randint(3, 8)
        elif difficulty == "intermediate":
            base = random.randint(5, 15)
            height = random.randint(4, 12)
        else:  # advanced
            base = random.randint(8, 20)
            height = random.randint(6, 15)
            
        area = 0.5 * base * height
        
        problem = f""" TRIANGLE AREA PROBLEM

Find the area of a triangle with:
" Base = {base} units
" Height = {height} units

Formula: Area = (1/2) × base × height

Remember to substitute the values into the formula and calculate carefully.
Round your answer to 2 decimal places if necessary.
        """
        
        self.current_problem = {"type": "triangle", "base": base, "height": height}
        self.current_answer = round(area, 2)
        self.update_text_widget(self.geometry_problem_text, problem)
        
    def generate_square_problem(self, difficulty):
        if difficulty == "beginner":
            side = random.randint(3, 10)
        elif difficulty == "intermediate":
            side = random.randint(5, 15)
        else:  # advanced
            side = random.randint(8, 25)
            
        area = side * side
        
        problem = f""" SQUARE AREA PROBLEM

Find the area of a square with:
" Side length = {side} units

Formula: Area = side²

Calculate the area by squaring the side length.
        """
        
        self.current_problem = {"type": "square", "side": side}
        self.current_answer = area
        self.update_text_widget(self.geometry_problem_text, problem)
        
    def generate_rectangle_problem(self, difficulty):
        if difficulty == "beginner":
            length = random.randint(4, 10)
            width = random.randint(3, 8)
        elif difficulty == "intermediate":
            length = random.randint(6, 15)
            width = random.randint(4, 12)
        else:  # advanced
            length = random.randint(10, 25)
            width = random.randint(6, 18)
            
        area = length * width
        
        problem = f"""­ RECTANGLE AREA PROBLEM

Find the area of a rectangle with:
" Length = {length} units
" Width = {width} units

Formula: Area = length × width

Multiply the length and width to find the area.
        """
        
        self.current_problem = {"type": "rectangle", "length": length, "width": width}
        self.current_answer = area
        self.update_text_widget(self.geometry_problem_text, problem)
        
    def generate_circle_problem(self, difficulty):
        if difficulty == "beginner":
            radius = random.randint(2, 8)
        elif difficulty == "intermediate":
            radius = random.randint(4, 12)
        else:  # advanced
            radius = random.randint(6, 20)
            
        area = math.pi * radius * radius
        
        problem = f""" CIRCLE AREA PROBLEM

Find the area of a circle with:
" Radius = {radius} units

Formula: Area = À × radius²

Use À H 3.14159 for your calculation.
Round your answer to 2 decimal places.
        """
        
        self.current_problem = {"type": "circle", "radius": radius}
        self.current_answer = round(area, 2)
        self.update_text_widget(self.geometry_problem_text, problem)
        
    def check_geometry_answer(self):
        try:
            user_answer = float(self.geometry_answer_entry.get())
            tolerance = 0.01
            
            if abs(user_answer - self.current_answer) <= tolerance:
                feedback = f" Excellent! That's correct!\n\nYour answer: {user_answer}\nCorrect answer: {self.current_answer}\n\n"
                feedback += self.get_geometry_explanation()
                self.student_progress['geometry']['correct'] += 1
                self.adapt_difficulty_up()
            else:
                feedback = f" Not quite right. Try again!\n\nYour answer: {user_answer}\nCorrect answer: {self.current_answer}\n\n"
                feedback += " Review the formula and check your calculation."
                self.adapt_difficulty_down()
                
            self.student_progress['geometry']['total'] += 1
            self.student_progress['geometry']['topics_covered'].add(self.current_problem['type'])
            self.update_text_widget(self.geometry_feedback, feedback)
            
        except ValueError:
            self.update_text_widget(self.geometry_feedback, "Please enter a valid number.")
            
    def get_geometry_explanation(self):
        problem = self.current_problem
        explanation = "Step-by-step solution:\n"
        
        if problem['type'] == 'triangle':
            explanation += f"Area = (1/2) × base × height\n"
            explanation += f"Area = (1/2) × {problem['base']} × {problem['height']}\n"
            explanation += f"Area = {self.current_answer}"
        elif problem['type'] == 'square':
            explanation += f"Area = side²\n"
            explanation += f"Area = {problem['side']}²\n"
            explanation += f"Area = {self.current_answer}"
        elif problem['type'] == 'rectangle':
            explanation += f"Area = length × width\n"
            explanation += f"Area = {problem['length']} × {problem['width']}\n"
            explanation += f"Area = {self.current_answer}"
        elif problem['type'] == 'circle':
            explanation += f"Area = À × radius²\n"
            explanation += f"Area = À × {problem['radius']}²\n"
            explanation += f"Area = À × {problem['radius']**2}\n"
            explanation += f"Area = {self.current_answer}"
            
        return explanation
        
    def show_geometry_hint(self):
        problem = self.current_problem
        if problem['type'] == 'triangle':
            hint = f" Hint: Use the formula Area = (1/2) × base × height\nSubstitute: base = {problem['base']}, height = {problem['height']}"
        elif problem['type'] == 'square':
            hint = f" Hint: Use the formula Area = side²\nSubstitute: side = {problem['side']}"
        elif problem['type'] == 'rectangle':
            hint = f" Hint: Use the formula Area = length × width\nSubstitute: length = {problem['length']}, width = {problem['width']}"
        elif problem['type'] == 'circle':
            hint = f" Hint: Use the formula Area = À × radius²\nSubstitute: radius = {problem['radius']}, À H 3.14159"
            
        self.update_text_widget(self.geometry_feedback, hint)
        
    def generate_algebra_problem(self):
        difficulty = self.difficulty_var.get()
        
        if difficulty == "beginner":
            self.generate_simple_quadratic()
        elif difficulty == "intermediate":
            self.generate_intermediate_quadratic()
        else:  # advanced
            self.generate_advanced_quadratic()
            
        self.algebra_answer_entry.delete(0, tk.END)
        self.update_text_widget(self.algebra_feedback, "")
        
    def generate_simple_quadratic(self):
        # Generate simple factorable quadratics
        root1 = random.randint(-5, 5)
        root2 = random.randint(-5, 5)
        
        # Expand (x - root1)(x - root2) = x² - (root1 + root2)x + root1*root2
        a = 1
        b = -(root1 + root2)
        c = root1 * root2
        
        if b >= 0:
            b_str = f"+ {b}"
        else:
            b_str = f"- {abs(b)}"
            
        if c >= 0:
            c_str = f"+ {c}"
        else:
            c_str = f"- {abs(c)}"
            
        equation = f"x² {b_str}x {c_str} = 0"
        
        problem = f""" QUADRATIC EQUATION PROBLEM (Beginner)

Solve the quadratic equation:
{equation}

This equation can be solved by factoring or using the quadratic formula.

Enter your solutions separated by commas (e.g., 2, -3)
Order doesn't matter.
        """
        
        self.current_problem = {"type": "quadratic", "a": a, "b": b, "c": c, "equation": equation}
        self.current_answer = sorted([root1, root2])
        self.update_text_widget(self.algebra_problem_text, problem)
        
    def generate_intermediate_quadratic(self):
        # Generate quadratics with integer coefficients
        a = random.choice([1, 2, 3])
        b = random.randint(-10, 10)
        c = random.randint(-8, 8)
        
        # Calculate discriminant to ensure real solutions
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            c = random.randint(-3, 3)  # Adjust to ensure real solutions
            
        solutions = self.solve_quadratic(a, b, c)
        
        equation = f"{a}x² "
        if b >= 0:
            equation += f"+ {b}x "
        else:
            equation += f"- {abs(b)}x "
        if c >= 0:
            equation += f"+ {c} = 0"
        else:
            equation += f"- {abs(c)} = 0"
            
        problem = f""" QUADRATIC EQUATION PROBLEM (Intermediate)

Solve the quadratic equation:
{equation}

Use the quadratic formula: x = (-b ± (b² - 4ac)) / (2a)
Where a = {a}, b = {b}, c = {c}

Enter your solutions separated by commas, rounded to 2 decimal places.
        """
        
        self.current_problem = {"type": "quadratic", "a": a, "b": b, "c": c, "equation": equation}
        self.current_answer = solutions
        self.update_text_widget(self.algebra_problem_text, problem)
        
    def generate_advanced_quadratic(self):
        # Generate more complex quadratics
        a = random.choice([2, 3, 4, 5])
        b = random.randint(-15, 15)
        c = random.randint(-10, 10)
        
        solutions = self.solve_quadratic(a, b, c)
        
        if solutions is None:
            # No real solutions, regenerate
            self.generate_advanced_quadratic()
            return
            
        equation = f"{a}x² "
        if b >= 0:
            equation += f"+ {b}x "
        else:
            equation += f"- {abs(b)}x "
        if c >= 0:
            equation += f"+ {c} = 0"
        else:
            equation += f"- {abs(c)} = 0"
            
        problem = f""" QUADRATIC EQUATION PROBLEM (Advanced)

Solve the quadratic equation:
{equation}

This may require careful application of the quadratic formula.
Consider whether the equation can be factored or if you need to use the formula.

Enter your solutions separated by commas, rounded to 2 decimal places.
        """
        
        self.current_problem = {"type": "quadratic", "a": a, "b": b, "c": c, "equation": equation}
        self.current_answer = solutions
        self.update_text_widget(self.algebra_problem_text, problem)
        
    def solve_quadratic(self, a, b, c):
        discriminant = b*b - 4*a*c
        
        if discriminant < 0:
            return None  # No real solutions
        elif discriminant == 0:
            solution = -b / (2*a)
            return [round(solution, 2)]
        else:
            sqrt_discriminant = math.sqrt(discriminant)
            solution1 = (-b + sqrt_discriminant) / (2*a)
            solution2 = (-b - sqrt_discriminant) / (2*a)
            return sorted([round(solution1, 2), round(solution2, 2)])
            
    def check_algebra_answer(self):
        try:
            user_input = self.algebra_answer_entry.get().strip()
            user_solutions = [round(float(x.strip()), 2) for x in user_input.split(',')]
            user_solutions.sort()
            
            correct_solutions = self.current_answer
            
            if user_solutions == correct_solutions:
                feedback = f" Excellent! That's correct!\n\nYour solutions: {user_solutions}\nCorrect solutions: {correct_solutions}\n\n"
                feedback += self.get_algebra_explanation()
                self.student_progress['algebra']['correct'] += 1
            else:
                feedback = f" Not quite right. Try again!\n\nYour solutions: {user_solutions}\nCorrect solutions: {correct_solutions}\n\n"
                feedback += " Check your calculation using the quadratic formula."
                
            self.student_progress['algebra']['total'] += 1
            self.student_progress['algebra']['topics_covered'].add('quadratic_equations')
            self.update_text_widget(self.algebra_feedback, feedback)
            
        except (ValueError, AttributeError):
            self.update_text_widget(self.algebra_feedback, "Please enter valid numbers separated by commas (e.g., 2.5, -1.3)")
            
    def get_algebra_explanation(self):
        problem = self.current_problem
        a, b, c = problem['a'], problem['b'], problem['c']
        
        explanation = f"Step-by-step solution using the quadratic formula:\n\n"
        explanation += f"Given: {problem['equation']}\n"
        explanation += f"Where a = {a}, b = {b}, c = {c}\n\n"
        explanation += f"Quadratic formula: x = (-b ± (b² - 4ac)) / (2a)\n\n"
        
        discriminant = b*b - 4*a*c
        explanation += f"Calculate discriminant: b² - 4ac = {b}² - 4({a})({c}) = {discriminant}\n\n"
        
        if discriminant > 0:
            sqrt_disc = math.sqrt(discriminant)
            explanation += f"x = (-{b} ± {discriminant}) / (2×{a})\n"
            explanation += f"x = ({-b} ± {sqrt_disc:.2f}) / {2*a}\n\n"
            
            x1 = (-b + sqrt_disc) / (2*a)
            x2 = (-b - sqrt_disc) / (2*a)
            explanation += f"x = ({-b} + {sqrt_disc:.2f}) / {2*a} = {x1:.2f}\n"
            explanation += f"x‚ = ({-b} - {sqrt_disc:.2f}) / {2*a} = {x2:.2f}"
        elif discriminant == 0:
            x = -b / (2*a)
            explanation += f"x = -{b} / (2×{a}) = {x:.2f}\n"
            explanation += "This equation has one repeated solution."
            
        return explanation
        
    def show_algebra_steps(self):
        explanation = self.get_algebra_explanation()
        self.update_text_widget(self.algebra_feedback, f" Solution Steps:\n\n{explanation}")
        
    def adapt_difficulty_up(self):
        """Increase difficulty if student is doing well"""
        geometry_rate = self.student_progress['geometry']['correct'] / max(1, self.student_progress['geometry']['total'])
        algebra_rate = self.student_progress['algebra']['correct'] / max(1, self.student_progress['algebra']['total'])
        overall_rate = (geometry_rate + algebra_rate) / 2
        
        if overall_rate > 0.8 and self.student_progress['difficulty_level'] == 'beginner':
            self.student_progress['difficulty_level'] = 'intermediate'
        elif overall_rate > 0.85 and self.student_progress['difficulty_level'] == 'intermediate':
            self.student_progress['difficulty_level'] = 'advanced'
            
    def adapt_difficulty_down(self):
        """Decrease difficulty if student is struggling"""
        total_problems = self.student_progress['geometry']['total'] + self.student_progress['algebra']['total']
        if total_problems < 5:  # Don't adjust too early
            return
            
        geometry_rate = self.student_progress['geometry']['correct'] / max(1, self.student_progress['geometry']['total'])
        algebra_rate = self.student_progress['algebra']['correct'] / max(1, self.student_progress['algebra']['total'])
        overall_rate = (geometry_rate + algebra_rate) / 2
        
        if overall_rate < 0.5 and self.student_progress['difficulty_level'] == 'advanced':
            self.student_progress['difficulty_level'] = 'intermediate'
        elif overall_rate < 0.4 and self.student_progress['difficulty_level'] == 'intermediate':
            self.student_progress['difficulty_level'] = 'beginner'
            
    def update_progress_display(self):
        progress_text = f"""=Ê LEARNING PROGRESS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

 CURRENT DIFFICULTY LEVEL: {self.student_progress['difficulty_level'].upper()}

 GEOMETRY PROGRESS:
" Problems Attempted: {self.student_progress['geometry']['total']}
" Problems Correct: {self.student_progress['geometry']['correct']}
" Success Rate: {(self.student_progress['geometry']['correct'] / max(1, self.student_progress['geometry']['total']) * 100):.1f}%
" Topics Covered: {', '.join(self.student_progress['geometry']['topics_covered']) if self.student_progress['geometry']['topics_covered'] else 'None yet'}

 ALGEBRA PROGRESS:
" Problems Attempted: {self.student_progress['algebra']['total']}
" Problems Correct: {self.student_progress['algebra']['correct']}
" Success Rate: {(self.student_progress['algebra']['correct'] / max(1, self.student_progress['algebra']['total']) * 100):.1f}%
" Topics Covered: {', '.join(self.student_progress['algebra']['topics_covered']) if self.student_progress['algebra']['topics_covered'] else 'None yet'}

 OVERALL PERFORMANCE:
" Total Problems: {self.student_progress['geometry']['total'] + self.student_progress['algebra']['total']}
" Total Correct: {self.student_progress['geometry']['correct'] + self.student_progress['algebra']['correct']}
" Overall Success Rate: {((self.student_progress['geometry']['correct'] + self.student_progress['algebra']['correct']) / max(1, self.student_progress['geometry']['total'] + self.student_progress['algebra']['total']) * 100):.1f}%

 RECOMMENDATIONS:
{self.get_learning_recommendations()}

 ADAPTIVE LEARNING STATUS:
The system automatically adjusts problem difficulty based on your performance.
Keep practicing to unlock more challenging problems!
        """
        
        self.update_text_widget(self.progress_text, progress_text)
        
    def get_learning_recommendations(self):
        recommendations = []
        
        # Geometry recommendations
        geometry_rate = self.student_progress['geometry']['correct'] / max(1, self.student_progress['geometry']['total'])
        if geometry_rate < 0.6:
            recommendations.append("" Review geometry formulas in the Help tab")
            recommendations.append("" Practice more basic area calculations")
        elif geometry_rate > 0.8:
            recommendations.append("" Great job with geometry! Try harder problems")
            
        # Algebra recommendations
        algebra_rate = self.student_progress['algebra']['correct'] / max(1, self.student_progress['algebra']['total'])
        if algebra_rate < 0.6:
            recommendations.append("" Focus on quadratic formula steps")
            recommendations.append("" Practice identifying coefficients a, b, c")
        elif algebra_rate > 0.8:
            recommendations.append("" Excellent algebra skills! Challenge yourself with advanced problems")
            
        # Topic coverage recommendations
        if len(self.student_progress['geometry']['topics_covered']) < 4:
            missing_shapes = set(['triangle', 'square', 'rectangle', 'circle']) - self.student_progress['geometry']['topics_covered']
            if missing_shapes:
                recommendations.append(f"" Try problems with: {', '.join(missing_shapes)}")
                
        if not recommendations:
            recommendations.append("" Keep up the excellent work!")
            recommendations.append("" Continue practicing to maintain your skills")
            
        return '\n'.join(recommendations)
        
    def update_text_widget(self, widget, text):
        widget.config(state='normal')
        widget.delete('1.0', tk.END)
        widget.insert('1.0', text)
        widget.config(state='disabled')

def main():
    root = tk.Tk()
    app = IntelligentTutoringSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()