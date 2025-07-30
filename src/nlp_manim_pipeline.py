"""
NLP to Manim Pipeline - Natural Language Animation Generation
Enhanced module for translating plain English to mathematically accurate animations
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import spacy
from sympy import symbols, simplify, latex
import numpy as np

class AnimationType(Enum):
    """Types of animations supported"""
    GEOMETRIC_TRANSFORM = "geometric_transform"
    VECTOR_OPERATION = "vector_operation"
    MANIFOLD_VISUALIZATION = "manifold_visualization"
    FIELD_DYNAMICS = "field_dynamics"
    ALGEBRAIC_STRUCTURE = "algebraic_structure"

@dataclass
class AnimationRequest:
    """Structured representation of animation request"""
    description: str
    animation_type: AnimationType
    objects: List[Dict[str, Any]]
    transformations: List[Dict[str, Any]]
    parameters: Dict[str, Any]
    validation_required: bool = True

class NLPAnimationParser:
    """Parse natural language descriptions into structured animation requests"""
    
    def __init__(self):
        # Load spaCy model for NLP
        self.nlp = spacy.load("en_core_web_sm")
        
        # Mathematical concept patterns
        self.concept_patterns = {
            "stereographic_projection": [
                r"stereo(?:graphic)?\s+project(?:ed|ion)?",
                r"project\s+.*\s+(?:on|onto)\s+.*\s+plane"
            ],
            "gyrovector_operation": [
                r"gyro(?:addition|scalar|distance|parallel)",
                r"(?:add|multiply|transport)\s+.*\s+gyrovector"
            ],
            "rotation": [
                r"rotate\s+.*\s+(?:around|about|relative)",
                r"(?:spin|turn)\s+.*\s+(?:by|through)"
            ],
            "mobius_transformation": [
                r"(?:mobius|möbius)\s+transform",
                r"conformal\s+map"
            ],
            "hyperbolic_space": [
                r"(?:poincaré|klein|hyperboloid)\s+(?:disk|ball|model)",
                r"hyperbolic\s+(?:plane|space|geometry)"
            ]
        }
        
        # Object extraction patterns
        self.object_patterns = {
            "sphere": r"S[²³⁴]?\s*sphere|(?:unit\s+)?sphere",
            "plane": r"(?:polar|complex|euclidean)?\s*plane",
            "vector": r"\[[\d.,\s-]+\]|vector\s*\([\d.,\s-]+\)",
            "point": r"point\s*(?:at\s*)?\([\d.,\s-]+\)",
            "manifold": r"(?:manifold|surface|space)"
        }

    def parse(self, description: str) -> AnimationRequest:
        """Parse natural language description into structured request"""
        # Normalize text
        description = description.lower().strip()
        
        # Detect animation type
        animation_type = self._detect_animation_type(description)
        
        # Extract objects
        objects = self._extract_objects(description)
        
        # Extract transformations
        transformations = self._extract_transformations(description)
        
        # Extract parameters
        parameters = self._extract_parameters(description)
        
        # Validate mathematical consistency
        self._validate_request(objects, transformations, parameters)
        
        return AnimationRequest(
            description=description,
            animation_type=animation_type,
            objects=objects,
            transformations=transformations,
            parameters=parameters
        )
    
    def _detect_animation_type(self, text: str) -> AnimationType:
        """Detect the type of animation requested"""
        for concept, patterns in self.concept_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    if "stereo" in concept or "mobius" in concept:
                        return AnimationType.GEOMETRIC_TRANSFORM
                    elif "gyro" in concept:
                        return AnimationType.VECTOR_OPERATION
                    elif "hyperbolic" in concept:
                        return AnimationType.MANIFOLD_VISUALIZATION
        
        return AnimationType.GEOMETRIC_TRANSFORM  # Default
    
    def _extract_objects(self, text: str) -> List[Dict[str, Any]]:
        """Extract mathematical objects from text"""
        objects = []
        
        # Parse with spaCy
        doc = self.nlp(text)
        
        # Extract based on patterns
        for obj_type, pattern in self.object_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                obj = {
                    "type": obj_type,
                    "value": match.group(),
                    "position": match.span()
                }
                
                # Parse vectors/points
                if obj_type in ["vector", "point"]:
                    coords = self._parse_coordinates(match.group())
                    if coords:
                        obj["coordinates"] = coords
                
                objects.append(obj)
        
        return objects
    
    def _extract_transformations(self, text: str) -> List[Dict[str, Any]]:
        """Extract transformations to apply"""
        transformations = []
        
        # Check for each transformation type
        transform_keywords = {
            "rotation": ["rotate", "spin", "turn"],
            "projection": ["project", "map"],
            "translation": ["move", "shift", "translate"],
            "scaling": ["scale", "resize", "zoom"]
        }
        
        for transform_type, keywords in transform_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    # Extract parameters for this transformation
                    transform = {
                        "type": transform_type,
                        "keyword": keyword,
                        "parameters": self._extract_transform_params(text, keyword)
                    }
                    transformations.append(transform)
        
        return transformations
    
    def _extract_parameters(self, text: str) -> Dict[str, Any]:
        """Extract animation parameters"""
        params = {
            "duration": 3.0,  # Default
            "quality": "standard",
            "style": "academic"
        }
        
        # Duration extraction
        duration_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:second|sec)s?", text)
        if duration_match:
            params["duration"] = float(duration_match.group(1))
        
        # Quality keywords
        if any(word in text for word in ["4k", "high quality", "ultra"]):
            params["quality"] = "4k"
        elif "preview" in text or "quick" in text:
            params["quality"] = "preview"
        
        # Style detection
        if "artistic" in text or "beautiful" in text:
            params["style"] = "artistic"
        elif "minimal" in text or "simple" in text:
            params["style"] = "minimalist"
        
        return params
    
    def _parse_coordinates(self, coord_str: str) -> Optional[List[float]]:
        """Parse coordinate strings like '[0.3, 0.4, 0]'"""
        try:
            # Remove brackets and parse
            coords = coord_str.strip("[]() ")
            return [float(x.strip()) for x in coords.split(",")]
        except:
            return None
    
    def _extract_transform_params(self, text: str, keyword: str) -> Dict[str, Any]:
        """Extract parameters for a specific transformation"""
        params = {}
        
        # Find context around keyword
        keyword_pos = text.find(keyword)
        context = text[max(0, keyword_pos-50):min(len(text), keyword_pos+50)]
        
        # Extract angles for rotations
        if keyword in ["rotate", "spin", "turn"]:
            angle_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:degree|rad|°)", context)
            if angle_match:
                params["angle"] = float(angle_match.group(1))
                params["unit"] = "degrees" if "°" in angle_match.group() else "radians"
        
        # Extract reference objects
        if "relative to" in context or "around" in context:
            ref_match = re.search(r"(?:relative to|around)\s+(?:the\s+)?(\w+)", context)
            if ref_match:
                params["reference"] = ref_match.group(1)
        
        return params
    
    def _validate_request(self, objects: List[Dict], 
                         transformations: List[Dict], 
                         parameters: Dict) -> None:
        """Validate mathematical consistency of request"""
        # Check object compatibility with transformations
        for transform in transformations:
            if transform["type"] == "stereographic_projection":
                # Ensure we have a sphere object
                sphere_objects = [o for o in objects if "sphere" in o["type"]]
                if not sphere_objects:
                    raise ValueError("Stereographic projection requires a sphere object")
        
        # Validate vector dimensions
        vectors = [o for o in objects if o["type"] == "vector"]
        if vectors:
            dimensions = [len(v.get("coordinates", [])) for v in vectors]
            if dimensions and len(set(dimensions)) > 1:
                raise ValueError("All vectors must have the same dimension")


class ManimCodeGenerator:
    """Generate Manim code from structured animation requests"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def generate(self, request: AnimationRequest) -> str:
        """Generate Manim code from animation request"""
        # Select appropriate template
        template = self._select_template(request)
        
        # Generate scene setup
        scene_code = self._generate_scene_setup(request)
        
        # Generate object creation code
        object_code = self._generate_objects(request.objects)
        
        # Generate transformation code
        transform_code = self._generate_transformations(
            request.transformations, 
            request.objects
        )
        
        # Combine into complete Manim script
        manim_code = f"""
from manim import *
import numpy as np
from math import *

class GeneratedAnimation(ThreeDScene):
    def construct(self):
        {scene_code}
        
        # Create objects
        {object_code}
        
        # Apply transformations
        {transform_code}
        
        # Render with appropriate timing
        self.wait({request.parameters.get('duration', 3)})
"""
        
        return manim_code
    
    def _load_templates(self) -> Dict[str, str]:
        """Load Manim code templates"""
        return {
            "stereographic_projection": '''
        # Stereographic projection setup
        sphere = Sphere(radius=2, resolution=(30, 30))
        sphere.set_color(BLUE_E)
        
        # Create projection plane
        plane = Square(side_length=6).rotate(PI/2, RIGHT)
        plane.shift(3*DOWN)
        plane.set_fill(GRAY, opacity=0.3)
        
        # Projection mapping function
        def stereo_project(point):
            x, y, z = point
            if z >= 0.99:  # Handle north pole
                return np.array([0, 0, -3])
            factor = 1 / (1 - z)
            return np.array([factor * x, factor * y, -3])
        ''',
            
            "gyrovector_addition": '''
        # Gyrovector addition in Poincaré disk
        disk = Circle(radius=3, color=WHITE)
        
        # Convert to Poincaré disk coordinates
        def to_poincare(v):
            norm = np.linalg.norm(v)
            if norm >= 1:
                return 0.99 * v / norm
            return v
        
        # Gyroaddition formula
        def gyro_add(u, v):
            u_norm_sq = np.dot(u, u)
            v_norm_sq = np.dot(v, v)
            uv_dot = np.dot(u, v)
            
            denominator = 1 + 2*uv_dot + u_norm_sq * v_norm_sq
            numerator_u = (1 + 2*uv_dot + v_norm_sq) * u
            numerator_v = (1 - u_norm_sq) * v
            
            return (numerator_u + numerator_v) / denominator
        '''
        }
    
    def _select_template(self, request: AnimationRequest) -> str:
        """Select appropriate template based on request type"""
        if request.animation_type == AnimationType.GEOMETRIC_TRANSFORM:
            for transform in request.transformations:
                if "project" in transform.get("keyword", ""):
                    return self.templates.get("stereographic_projection", "")
        elif request.animation_type == AnimationType.VECTOR_OPERATION:
            return self.templates.get("gyrovector_addition", "")
        
        return ""  # Default empty template
    
    def _generate_scene_setup(self, request: AnimationRequest) -> str:
        """Generate scene setup code"""
        setup_code = []
        
        # Camera setup based on content
        if request.animation_type == AnimationType.MANIFOLD_VISUALIZATION:
            setup_code.append("""
        # 3D camera setup
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        """)
        
        # Lighting and style
        if request.parameters.get("style") == "artistic":
            setup_code.append("""
        # Artistic lighting
        self.camera.background_color = "#1e1e2e"
        """)
        
        return "\n".join(setup_code)
    
    def _generate_objects(self, objects: List[Dict]) -> str:
        """Generate code for creating objects"""
        object_code = []
        
        for i, obj in enumerate(objects):
            obj_name = f"obj_{i}"
            
            if obj["type"] == "sphere":
                # Parse sphere notation (S², S³, etc.)
                dimension = 3  # Default
                if "S²" in obj["value"] or "S^2" in obj["value"]:
                    dimension = 2
                elif "S³" in obj["value"] or "S^3" in obj["value"]:
                    dimension = 3
                
                object_code.append(f"""
        {obj_name} = Sphere(radius=2, resolution=(30, 30))
        {obj_name}.set_color(BLUE_E)
        self.add({obj_name})
        """)
            
            elif obj["type"] == "vector" and "coordinates" in obj:
                coords = obj["coordinates"]
                object_code.append(f"""
        {obj_name}_coords = {coords}
        {obj_name} = Arrow3D(ORIGIN, {obj_name}_coords, color=YELLOW)
        self.add({obj_name})
        """)
            
            elif obj["type"] == "plane":
                plane_type = "polar" if "polar" in obj["value"] else "standard"
                object_code.append(f"""
        {obj_name} = Square(side_length=6).rotate(PI/2, RIGHT)
        {obj_name}.shift(3*DOWN)
        {obj_name}.set_fill(GRAY, opacity=0.3)
        self.add({obj_name})
        """)
        
        return "\n".join(object_code)
    
    def _generate_transformations(self, transformations: List[Dict], 
                                 objects: List[Dict]) -> str:
        """Generate transformation code"""
        transform_code = []
        
        for transform in transformations:
            if transform["type"] == "rotation":
                angle = transform["parameters"].get("angle", 360)
                unit = transform["parameters"].get("unit", "degrees")
                
                if unit == "degrees":
                    angle_rad = f"{angle}*DEGREES"
                else:
                    angle_rad = str(angle)
                
                transform_code.append(f"""
        # Rotation animation
        self.play(
            Rotate(obj_0, {angle_rad}, axis=UP, about_point=ORIGIN),
            run_time=3
        )
        """)
            
            elif transform["type"] == "projection":
                transform_code.append("""
        # Stereographic projection animation
        projected_points = []
        for point in sphere.get_points():
            projected = stereo_project(point)
            projected_points.append(projected)
        
        # Animate projection
        self.play(
            *[Transform(
                Dot(point), 
                Dot(projected)
            ) for point, projected in zip(
                sphere.get_points()[::10], 
                projected_points[::10]
            )],
            run_time=4
        )
        """)
        
        return "\n".join(transform_code)


class AnimationValidator:
    """Validate mathematical accuracy of animations"""
    
    def __init__(self):
        self.wolfram_client = None  # Initialize with actual Wolfram client
    
    def validate(self, request: AnimationRequest, 
                generated_code: str) -> Dict[str, Any]:
        """Validate the mathematical accuracy of generated animation"""
        validation_results = {
            "mathematical_accuracy": True,
            "warnings": [],
            "suggestions": []
        }
        
        # Validate based on animation type
        if request.animation_type == AnimationType.VECTOR_OPERATION:
            validation_results.update(
                self._validate_vector_operations(request)
            )
        elif request.animation_type == AnimationType.GEOMETRIC_TRANSFORM:
            validation_results.update(
                self._validate_geometric_transforms(request)
            )
        
        # Check numerical stability
        stability_check = self._check_numerical_stability(generated_code)
        if not stability_check["stable"]:
            validation_results["warnings"].append(
                f"Potential numerical instability: {stability_check['reason']}"
            )
        
        return validation_results
    
    def _validate_vector_operations(self, request: AnimationRequest) -> Dict:
        """Validate vector operations"""
        results = {}
        
        # Extract vectors from request
        vectors = [obj for obj in request.objects if obj["type"] == "vector"]
        
        if len(vectors) >= 2 and all("coordinates" in v for v in vectors):
            # Check if vectors are in valid range for gyrovector operations
            for v in vectors:
                norm = np.linalg.norm(v["coordinates"])
                if norm >= 1:
                    results["warnings"] = results.get("warnings", [])
                    results["warnings"].append(
                        f"Vector {v['coordinates']} has norm >= 1, "
                        "not valid for Poincaré ball model"
                    )
        
        return results
    
    def _validate_geometric_transforms(self, request: AnimationRequest) -> Dict:
        """Validate geometric transformations"""
        results = {}
        
        # Check for stereographic projection validity
        for transform in request.transformations:
            if transform["type"] == "projection":
                # Ensure we're not projecting from the projection point
                results["suggestions"] = results.get("suggestions", [])
                results["suggestions"].append(
                    "Consider handling the north pole singularity "
                    "in stereographic projection"
                )
        
        return results
    
    def _check_numerical_stability(self, code: str) -> Dict[str, Any]:
        """Check for potential numerical instabilities"""
        stability_issues = []
        
        # Check for division by small numbers
        if "/ (1 -" in code and "0.99" not in code:
            stability_issues.append("Division by (1-z) without bounds check")
        
        # Check for normalization of near-zero vectors
        if "norm(" in code and "if norm" not in code:
            stability_issues.append("Vector normalization without zero check")
        
        return {
            "stable": len(stability_issues) == 0,
            "reason": "; ".join(stability_issues) if stability_issues else None
        }


# Main pipeline function
def process_animation_request(description: str, 
                            validate: bool = True) -> Dict[str, Any]:
    """
    Main entry point for NLP to Manim pipeline
    
    Args:
        description: Natural language description of desired animation
        validate: Whether to perform mathematical validation
    
    Returns:
        Dictionary containing:
        - manim_code: Generated Manim Python code
        - validation_report: Mathematical validation results
        - animation_request: Structured representation of request
    """
    # Initialize components
    parser = NLPAnimationParser()
    generator = ManimCodeGenerator()
    validator = AnimationValidator()
    
    try:
        # Parse natural language
        animation_request = parser.parse(description)
        
        # Generate Manim code
        manim_code = generator.generate(animation_request)
        
        # Validate if requested
        validation_report = {}
        if validate:
            validation_report = validator.validate(
                animation_request, 
                manim_code
            )
        
        return {
            "success": True,
            "manim_code": manim_code,
            "validation_report": validation_report,
            "animation_request": animation_request.__dict__
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "manim_code": None,
            "validation_report": {"error": str(e)},
            "animation_request": None
        }


# Example usage
if __name__ == "__main__":
    # Test with example descriptions
    examples = [
        "Create an animation showing a stereo projected S³ sphere on a polar plane, then rotate the plane relative to the pole",
        "Show gyroaddition of [0.3,0.4,0] and [0.1,0.2,0.5] in the Poincaré ball model",
        "Visualize a Möbius transformation on the complex plane with parameters a=1, b=2, c=3, d=4"
    ]
    
    for example in examples:
        print(f"\n{'='*60}")
        print(f"Processing: {example}")
        print('='*60)
        
        result = process_animation_request(example)
        
        if result["success"]:
            print("✓ Successfully generated Manim code")
            print(f"Animation type: {result['animation_request']['animation_type']}")
            print(f"Objects detected: {len(result['animation_request']['objects'])}")
            print(f"Transformations: {len(result['animation_request']['transformations'])}")
            
            if result["validation_report"]:
                print(f"Validation: {result['validation_report']}")
        else:
            print(f"✗ Error: {result['error']}")
