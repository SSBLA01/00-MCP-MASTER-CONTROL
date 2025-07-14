from manim import *
import numpy as np

class GyrovectorCleanAnimation(Scene):
    def construct(self):
        # Configuration
        self.camera.background_color = "#0a0a0a"
        
        # Create title that stays at top
        title = Text("Gyrovector Addition in Poincaré Disk", font_size=32)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # Create the Poincaré disk
        disk = Circle(radius=2.5, color=BLUE_B, stroke_width=4)
        disk.shift(LEFT * 2)  # Shift disk to left to make room for formulas
        
        # Create disk and keep it visible
        self.play(Create(disk))
        self.wait(0.5)
        
        # Points for gyrovector addition
        a = np.array([0.3, 0.2, 0])
        b = np.array([-0.2, 0.3, 0])
        
        # Simple Möbius addition
        def mobius_add_simple(u, v):
            u_c = complex(u[0], u[1])
            v_c = complex(v[0], v[1])
            result = (u_c + v_c) / (1 + np.conj(u_c) * v_c)
            return np.array([result.real, result.imag, 0])
        
        c = mobius_add_simple(a, b)
        
        # Create dots (shifted with disk)
        dot_a = Dot((a * 2.5) + LEFT * 2, color=YELLOW, radius=0.1)
        dot_b = Dot((b * 2.5) + LEFT * 2, color=GREEN, radius=0.1)
        dot_c = Dot((c * 2.5) + LEFT * 2, color=RED, radius=0.1)
        
        # Create labels with proper spacing
        label_a = MathTex("a", color=YELLOW).scale(0.8)
        label_b = MathTex("b", color=GREEN).scale(0.8)
        label_c = MathTex("a \\oplus b", color=RED).scale(0.8)
        
        # Position labels to avoid overlap
        label_a.next_to(dot_a, RIGHT, buff=0.2)
        label_b.next_to(dot_b, LEFT, buff=0.2)
        label_c.next_to(dot_c, DOWN, buff=0.2)
        
        # Add dots and labels
        self.play(
            FadeIn(dot_a), 
            FadeIn(dot_b), 
            Write(label_a), 
            Write(label_b)
        )
        self.wait(0.5)
        
        # Create formula area on the right
        formula_area = VGroup()
        
        # Formula title
        formula_title = Text("Möbius Addition:", font_size=24)
        formula_title.shift(RIGHT * 3.5)
        
        # The formula itself (smaller to fit better)
        formula = MathTex(
            "a \\oplus b = \\frac{a + b}{1 + \\overline{a}b}",
            font_size=28
        )
        formula.next_to(formula_title, DOWN, buff=0.5)
        
        formula_area.add(formula_title, formula)
        
        # Show formula
        self.play(Write(formula_title))
        self.play(Write(formula))
        self.wait(0.5)
        
        # Draw lines (shifted with disk)
        line_a = Line(LEFT * 2, (a * 2.5) + LEFT * 2, color=YELLOW, stroke_width=2)
        line_b = Line(LEFT * 2, (b * 2.5) + LEFT * 2, color=GREEN, stroke_width=2)
        line_c = Line(LEFT * 2, (c * 2.5) + LEFT * 2, color=RED, stroke_width=2)
        
        self.play(Create(line_a), Create(line_b))
        self.wait(0.5)
        
        # Show result
        self.play(
            Create(line_c),
            FadeIn(dot_c),
            Write(label_c)
        )
        self.wait(1)
        
        # Add property text below formula
        property_text = Text("Non-commutative:", font_size=20, color=ORANGE)
        property_text.next_to(formula, DOWN, buff=0.8)
        
        property_formula = MathTex(
            "a \\oplus b \\neq b \\oplus a",
            font_size=24,
            color=ORANGE
        )
        property_formula.next_to(property_text, DOWN, buff=0.3)
        
        self.play(Write(property_text))
        self.play(Write(property_formula))
        
        # Keep everything visible for a moment
        self.wait(3)
        
        # Final fade out (optional)
        # self.play(*[FadeOut(mob) for mob in self.mobjects])
