#!/usr/bin/env python3
"""
Patient Symptom Diagnosis Application
Multi-layer symptom analysis for disease diagnosis
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Tuple


# ============================================================================
# DISEASE DATABASE
# ============================================================================

DISEASES = {
    "common_cold": {
        "name": "Common Cold",
        "symptoms": ["cough", "runny_nose", "sore_throat", "fatigue", "headache"],
        "description": "Viral infection of upper respiratory tract",
        "severity": "Mild",
        "recovery_time": "7-10 days"
    },
    "flu": {
        "name": "Flu (Influenza)",
        "symptoms": ["fever", "cough", "muscle_pain", "fatigue", "headache", "sore_throat"],
        "description": "Viral infection affecting respiratory system",
        "severity": "Moderate",
        "recovery_time": "7-14 days"
    },
    "migraine": {
        "name": "Migraine",
        "symptoms": ["severe_headache", "nausea", "light_sensitivity", "fatigue", "vision_changes"],
        "description": "Severe headache with associated symptoms",
        "severity": "Moderate to Severe",
        "recovery_time": "4-72 hours"
    },
    "tension_headache": {
        "name": "Tension Headache",
        "symptoms": ["headache", "neck_stiffness", "fatigue", "difficulty_concentrating"],
        "description": "Most common type of headache",
        "severity": "Mild to Moderate",
        "recovery_time": "30 mins to several hours"
    },
    "covid_19": {
        "name": "COVID-19",
        "symptoms": ["fever", "cough", "fatigue", "loss_of_taste", "loss_of_smell", "difficulty_breathing"],
        "description": "Viral infection caused by SARS-CoV-2",
        "severity": "Mild to Severe",
        "recovery_time": "7-14 days or more"
    },
    "pneumonia": {
        "name": "Pneumonia",
        "symptoms": ["fever", "cough", "chest_pain", "difficulty_breathing", "fatigue"],
        "description": "Lung infection that fills air sacs with fluid",
        "severity": "Severe",
        "recovery_time": "2-4 weeks"
    },
    "bronchitis": {
        "name": "Bronchitis",
        "symptoms": ["cough", "chest_pain", "fatigue", "wheezing", "difficulty_breathing"],
        "description": "Inflammation of bronchial tubes in lungs",
        "severity": "Moderate",
        "recovery_time": "2-3 weeks"
    },
    "arthritis": {
        "name": "Arthritis",
        "symptoms": ["joint_pain", "swelling", "stiffness", "fatigue", "muscle_pain"],
        "description": "Inflammation of one or more joints",
        "severity": "Mild to Moderate",
        "recovery_time": "Chronic condition"
    },
    "gastroenteritis": {
        "name": "Gastroenteritis (Food Poisoning)",
        "symptoms": ["nausea", "vomiting", "diarrhea", "abdominal_pain", "fever"],
        "description": "Stomach and intestinal inflammation",
        "severity": "Mild to Moderate",
        "recovery_time": "1-3 days"
    },
    "peptic_ulcer": {
        "name": "Peptic Ulcer",
        "symptoms": ["abdominal_pain", "nausea", "loss_of_appetite", "bloating"],
        "description": "Open sore in stomach lining",
        "severity": "Moderate",
        "recovery_time": "4-6 weeks with treatment"
    },
    "measles": {
        "name": "Measles",
        "symptoms": ["fever", "cough", "rash", "runny_nose", "red_eyes"],
        "description": "Highly contagious viral infection",
        "severity": "Moderate to Severe",
        "recovery_time": "7-10 days"
    },
    "chickenpox": {
        "name": "Chickenpox",
        "symptoms": ["fever", "rash", "fatigue", "headache", "loss_of_appetite"],
        "description": "Viral infection causing chickenpox rash",
        "severity": "Mild to Moderate",
        "recovery_time": "7-10 days"
    },
    "dengue": {
        "name": "Dengue Fever",
        "symptoms": ["fever", "headache", "muscle_pain", "joint_pain", "rash"],
        "description": "Mosquito-borne viral infection",
        "severity": "Moderate to Severe",
        "recovery_time": "7-14 days"
    },
    "heart_attack": {
        "name": "Heart Attack",
        "symptoms": ["chest_pain", "shortness_of_breath", "arm_pain", "nausea", "fatigue"],
        "description": "Life-threatening emergency condition",
        "severity": "CRITICAL",
        "recovery_time": "Variable"
    },
    "asthma": {
        "name": "Asthma",
        "symptoms": ["wheezing", "difficulty_breathing", "chest_tightness", "cough"],
        "description": "Chronic respiratory condition",
        "severity": "Mild to Severe",
        "recovery_time": "Chronic condition"
    },
    "anxiety": {
        "name": "Anxiety Disorder",
        "symptoms": ["difficulty_breathing", "chest_pain", "dizziness", "fatigue", "muscle_pain"],
        "description": "Mental health condition causing physical symptoms",
        "severity": "Mild to Moderate",
        "recovery_time": "Variable with treatment"
    }
}

# Symptom mapping to disease keywords
SYMPTOM_DISEASE_MAP = {
    "cough": ["common_cold", "flu", "covid_19", "pneumonia", "bronchitis", "measles", "asthma"],
    "runny_nose": ["common_cold", "measles"],
    "sore_throat": ["common_cold", "flu"],
    "fatigue": ["common_cold", "flu", "covid_19", "pneumonia", "measles", "chickenpox", "dengue", "anxiety", "heart_attack"],
    "headache": ["common_cold", "flu", "migraine", "tension_headache", "covid_19", "dengue", "measles", "chickenpox"],
    "fever": ["flu", "covid_19", "pneumonia", "measles", "chickenpox", "dengue", "gastroenteritis"],
    "muscle_pain": ["flu", "dengue", "arthritis"],
    "loss_of_taste": ["covid_19"],
    "loss_of_smell": ["covid_19"],
    "difficulty_breathing": ["pneumonia", "bronchitis", "covid_19", "asthma", "anxiety", "heart_attack"],
    "chest_pain": ["pneumonia", "bronchitis", "heart_attack", "anxiety"],
    "wheezing": ["bronchitis", "asthma"],
    "joint_pain": ["arthritis", "dengue", "flu"],
    "swelling": ["arthritis"],
    "stiffness": ["arthritis", "tension_headache"],
    "nausea": ["migraine", "gastroenteritis", "peptic_ulcer", "heart_attack"],
    "vomiting": ["gastroenteritis"],
    "diarrhea": ["gastroenteritis", "covid_19"],
    "abdominal_pain": ["gastroenteritis", "peptic_ulcer"],
    "loss_of_appetite": ["peptic_ulcer", "measles", "chickenpox"],
    "bloating": ["peptic_ulcer"],
    "rash": ["measles", "chickenpox", "dengue"],
    "red_eyes": ["measles"],
    "light_sensitivity": ["migraine"],
    "vision_changes": ["migraine"],
    "difficulty_concentrating": ["tension_headache"],
    "neck_stiffness": ["tension_headache"],
    "arm_pain": ["heart_attack"],
    "chest_tightness": ["asthma"],
    "dizziness": ["anxiety"],
    "shortness_of_breath": ["heart_attack"]
}


# ============================================================================
# LAYER DEFINITIONS
# ============================================================================

LAYERS = {
    "primary_symptoms": {
        "name": "Primary Symptoms",
        "items": {
            "headache": {"name": "Headache", "next_layer": "headache_details"},
            "fever": {"name": "Fever", "next_layer": "fever_details"},
            "cough": {"name": "Cough", "next_layer": "cough_details"},
            "joint_pain": {"name": "Joint Pain", "next_layer": "joint_details"},
            "nausea_vomiting": {"name": "Nausea/Vomiting", "next_layer": "nausea_details"},
            "chest_pain": {"name": "Chest Pain", "next_layer": "chest_pain_details"},
            "breathing_issues": {"name": "Difficulty Breathing", "next_layer": "breathing_details"},
            "rash": {"name": "Rash", "next_layer": "rash_details"},
            "fatigue": {"name": "Fatigue", "next_layer": "fatigue_details"}
        }
    },
    
    "headache_details": {
        "name": "Headache Details - Location",
        "items": {
            "frontal": {"name": "Front of head", "questions": ["severity", "duration"]},
            "temporal": {"name": "Temples/Sides", "questions": ["severity", "duration", "light_sensitivity"]},
            "occipital": {"name": "Back of head", "questions": ["severity", "duration", "neck_stiffness"]},
            "all_over": {"name": "All over head", "questions": ["severity", "duration", "onset"]},
        }
    },
    
    "fever_details": {
        "name": "Fever Details - Temperature Level",
        "items": {
            "mild_fever": {"name": "Mild (98-100°F / 36.7-37.8°C)", "questions": ["duration", "other_symptoms"]},
            "moderate_fever": {"name": "Moderate (100-102°F / 37.8-39°C)", "questions": ["duration", "other_symptoms", "onset"]},
            "high_fever": {"name": "High (>102°F / >39°C)", "questions": ["duration", "onset", "exposure"]},
        }
    },
    
    "cough_details": {
        "name": "Cough Details - Type",
        "items": {
            "dry_cough": {"name": "Dry Cough (No mucus)", "questions": ["duration", "severity", "triggers"]},
            "wet_cough": {"name": "Wet Cough (With mucus)", "questions": ["mucus_color", "duration", "severity"]},
            "persistent_cough": {"name": "Persistent/Chronic", "questions": ["duration", "triggers", "wheezing"]},
        }
    },
    
    "joint_details": {
        "name": "Joint Pain Details - Location",
        "items": {
            "knee": {"name": "Knee", "questions": ["severity", "swelling", "movement_affected"]},
            "shoulder": {"name": "Shoulder", "questions": ["severity", "movement_range"]},
            "hip": {"name": "Hip", "questions": ["severity", "walking_affected"]},
            "multiple": {"name": "Multiple Joints", "questions": ["severity", "swelling", "morning_stiffness"]},
        }
    },
    
    "nausea_details": {
        "name": "Nausea/Vomiting Details",
        "items": {
            "nausea_only": {"name": "Nausea Only", "questions": ["frequency", "associated_symptoms"]},
            "frequent_vomiting": {"name": "Frequent Vomiting", "questions": ["content", "duration", "dehydration"]},
            "occasional_vomiting": {"name": "Occasional Vomiting", "questions": ["triggers", "duration"]},
        }
    },
    
    "chest_pain_details": {
        "name": "Chest Pain Details - Type & Location",
        "items": {
            "left_center": {"name": "Left/Center Chest", "questions": ["severity", "radiation", "triggers"]},
            "right_side": {"name": "Right Side", "questions": ["severity", "breathing_affects"]},
            "pressure": {"name": "Pressure/Tightness", "questions": ["severity", "radiation", "triggers"]},
        }
    },
    
    "breathing_details": {
        "name": "Breathing Difficulty - Type",
        "items": {
            "shortness_of_breath": {"name": "Shortness of Breath", "questions": ["exertion", "chest_pain", "onset"]},
            "wheezing": {"name": "Wheezing", "questions": ["triggers", "asthma_history", "chest_pain"]},
            "both": {"name": "Both", "questions": ["triggers", "onset", "medical_history"]},
        }
    },
    
    "rash_details": {
        "name": "Rash Details",
        "items": {
            "itchy_rash": {"name": "Itchy Rash", "questions": ["distribution", "fever"]},
            "red_bumps": {"name": "Red Bumps/Spots", "questions": ["fever", "spreading", "contagious_exposure"]},
            "painful_rash": {"name": "Painful Rash", "questions": ["location", "distribution"]},
        }
    },
    
    "fatigue_details": {
        "name": "Fatigue Details",
        "items": {
            "mild_fatigue": {"name": "Mild (Can do daily activities)", "questions": ["duration", "other_symptoms"]},
            "moderate_fatigue": {"name": "Moderate (Difficulty with activities)", "questions": ["duration", "sleep", "other_symptoms"]},
            "severe_fatigue": {"name": "Severe (Bedridden)", "questions": ["duration", "fever", "other_symptoms"]},
        }
    }
}


# ============================================================================
# QUESTION DEFINITIONS
# ============================================================================

QUESTIONS = {
    "severity": {
        "question": "How severe is your pain/discomfort?",
        "type": "multiple_choice",
        "options": ["Mild", "Moderate", "Severe"],
        "weights": {"Mild": 0.3, "Moderate": 0.6, "Severe": 0.9}
    },
    "duration": {
        "question": "How long have you had this symptom?",
        "type": "multiple_choice",
        "options": ["Less than 1 day", "1-2 days", "3-7 days", "More than 1 week"],
        "weights": {"Less than 1 day": 0.3, "1-2 days": 0.5, "3-7 days": 0.7, "More than 1 week": 0.9}
    },
    "onset": {
        "question": "Did the symptom start suddenly or gradually?",
        "type": "yes_no",
        "yes_text": "Sudden onset",
        "no_text": "Gradual onset",
        "weights": {"yes": 0.7, "no": 0.4}
    },
    "triggers": {
        "question": "Do you have any known triggers (allergens, stress, activity)?",
        "type": "yes_no",
        "weights": {"yes": 0.6, "no": 0.3}
    },
    "light_sensitivity": {
        "question": "Are you sensitive to light?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.2}
    },
    "neck_stiffness": {
        "question": "Do you have neck stiffness?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.2}
    },
    "other_symptoms": {
        "question": "Do you have any other symptoms (cough, body aches, sore throat)?",
        "type": "yes_no",
        "weights": {"yes": 0.7, "no": 0.3}
    },
    "exposure": {
        "question": "Have you been exposed to sick people recently?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.2}
    },
    "mucus_color": {
        "question": "What color is the mucus?",
        "type": "multiple_choice",
        "options": ["Clear", "White/Yellowish", "Green/Yellow"],
        "weights": {"Clear": 0.3, "White/Yellowish": 0.6, "Green/Yellow": 0.9}
    },
    "wheezing": {
        "question": "Do you have wheezing sounds while breathing?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.2}
    },
    "swelling": {
        "question": "Is there swelling around the joint?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.3}
    },
    "movement_affected": {
        "question": "Is your movement/mobility affected?",
        "type": "yes_no",
        "weights": {"yes": 0.7, "no": 0.3}
    },
    "movement_range": {
        "question": "Is your range of motion limited?",
        "type": "yes_no",
        "weights": {"yes": 0.7, "no": 0.3}
    },
    "walking_affected": {
        "question": "Does it affect your walking?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.3}
    },
    "morning_stiffness": {
        "question": "Do you have morning stiffness?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.3}
    },
    "frequency": {
        "question": "How frequently are you experiencing nausea?",
        "type": "multiple_choice",
        "options": ["Occasionally", "Frequently", "Constantly"],
        "weights": {"Occasionally": 0.3, "Frequently": 0.6, "Constantly": 0.9}
    },
    "associated_symptoms": {
        "question": "Do you have associated symptoms (fever, diarrhea)?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.2}
    },
    "content": {
        "question": "Is there anything unusual in the vomit?",
        "type": "yes_no",
        "weights": {"yes": 0.7, "no": 0.3}
    },
    "dehydration": {
        "question": "Are you experiencing signs of dehydration (dry mouth, dark urine)?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.2}
    },
    "radiation": {
        "question": "Does the pain radiate to your arm, neck, or jaw?",
        "type": "yes_no",
        "weights": {"yes": 0.9, "no": 0.3}
    },
    "breathing_affects": {
        "question": "Does breathing affect the pain?",
        "type": "yes_no",
        "weights": {"yes": 0.7, "no": 0.4}
    },
    "exertion": {
        "question": "Does the breathlessness occur with exertion or at rest?",
        "type": "multiple_choice",
        "options": ["With exertion only", "Both exertion and rest", "At rest only"],
        "weights": {"With exertion only": 0.3, "Both exertion and rest": 0.7, "At rest only": 0.9}
    },
    "chest_pain": {
        "question": "Do you have chest pain along with breathing difficulty?",
        "type": "yes_no",
        "weights": {"yes": 0.9, "no": 0.2}
    },
    "asthma_history": {
        "question": "Do you have a history of asthma?",
        "type": "yes_no",
        "weights": {"yes": 0.9, "no": 0.2}
    },
    "medical_history": {
        "question": "Do you have any chronic medical conditions?",
        "type": "yes_no",
        "weights": {"yes": 0.6, "no": 0.2}
    },
    "distribution": {
        "question": "Where is the rash located?",
        "type": "multiple_choice",
        "options": ["Localized area", "Spreading across body", "All over body"],
        "weights": {"Localized area": 0.3, "Spreading across body": 0.6, "All over body": 0.9}
    },
    "fever": {
        "question": "Do you have a fever along with this?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.2}
    },
    "spreading": {
        "question": "Is the rash spreading?",
        "type": "yes_no",
        "weights": {"yes": 0.7, "no": 0.3}
    },
    "contagious_exposure": {
        "question": "Have you been exposed to contagious illnesses?",
        "type": "yes_no",
        "weights": {"yes": 0.8, "no": 0.2}
    },
    "sleep": {
        "question": "Is fatigue affecting your sleep?",
        "type": "yes_no",
        "weights": {"yes": 0.7, "no": 0.3}
    },
}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_header(text: str):
    """Display a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def display_menu(title: str, items: Dict, show_back: bool = True) -> str:
    """Display a menu and get user selection."""
    print(f"\n{title}")
    print("-" * 60)
    
    options = list(items.keys())
    
    for i, option_key in enumerate(options, 1):
        option_data = items[option_key]
        if isinstance(option_data, dict) and "name" in option_data:
            print(f"{i}. {option_data['name']}")
        else:
            print(f"{i}. {option_key.replace('_', ' ').title()}")
    
    if show_back:
        print(f"{len(options) + 1}. Go Back")
    
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            elif choice == len(options) + 1 and show_back:
                return "back"
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def ask_yes_no_question(question_text: str) -> bool:
    """Ask a yes/no question and get response."""
    while True:
        response = input(f"\n{question_text}\n(yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")


def ask_multiple_choice(question_text: str, options: List[str]) -> str:
    """Ask a multiple choice question."""
    print(f"\n{question_text}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


# ============================================================================
# DIAGNOSIS ENGINE
# ============================================================================

class DiagnosisEngine:
    def __init__(self):
        self.selected_symptoms = []
        self.user_answers = {}
        self.layer_history = []
        self.confidence_scores = {}
    
    def calculate_confidence(self) -> Dict[str, float]:
        """Calculate confidence scores for each disease."""
        scores = {disease_key: 0.0 for disease_key in DISEASES.keys()}
        
        # Score based on selected symptoms
        for symptom in self.selected_symptoms:
            if symptom in SYMPTOM_DISEASE_MAP:
                for disease in SYMPTOM_DISEASE_MAP[symptom]:
                    scores[disease] += 0.5
        
        # Boost scores based on user answers
        for question_key, answer in self.user_answers.items():
            if question_key in QUESTIONS:
                question_data = QUESTIONS[question_key]
                if question_data["type"] == "yes_no":
                    if answer:
                        weight = question_data["weights"].get("yes", 0.5)
                    else:
                        weight = question_data["weights"].get("no", 0.5)
                elif question_data["type"] == "multiple_choice":
                    weight = question_data["weights"].get(answer, 0.5)
                else:
                    continue
                
                # Apply weight to relevant diseases
                for disease_key in DISEASES.keys():
                    scores[disease_key] += weight * 0.2
        
        # Normalize scores to percentage
        max_score = max(scores.values()) if scores.values() else 1
        if max_score > 0:
            scores = {k: (v / max_score) * 100 for k, v in scores.items()}
        
        return scores
    
    def start_diagnosis(self):
        """Start the diagnosis process."""
        clear_screen()
        display_header("PATIENT SYMPTOM DIAGNOSIS APP")
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║  Welcome to the Symptom Diagnosis Application               ║
║                                                              ║
║  ⚠️  IMPORTANT DISCLAIMER:                                   ║
║  This app is for INFORMATIONAL PURPOSES ONLY                ║
║  NOT a substitute for professional medical advice           ║
║  Always consult a healthcare professional                   ║
║  For emergencies, call emergency services immediately       ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        input("Press Enter to continue...")
        
        # Layer 1: Select Primary Symptom
        self.select_primary_symptoms()
        
        # Continue with multi-layer questions
        self.multi_layer_questions()
        
        # Show results
        self.show_results()
    
    def select_primary_symptoms(self):
        """Let patient select primary symptoms (Layer 1)."""
        clear_screen()
        display_header("LAYER 1: PRIMARY SYMPTOMS")
        
        print("Select all symptoms you are experiencing:")
        print("(Select 'Done' when finished)\n")
        
        layer_items = LAYERS["primary_symptoms"]["items"]
        selected_keys = []
        
        while True:
            print("\nSelected symptoms so far:")
            if selected_keys:
                for key in selected_keys:
                    print(f"  ✓ {layer_items[key]['name']}")
            else:
                print("  (None yet)")
            
            print("\nAvailable symptoms:")
            options = list(layer_items.keys())
            for i, option_key in enumerate(options, 1):
                status = "✓" if option_key in selected_keys else " "
                print(f"{i}. [{status}] {layer_items[option_key]['name']}")
            
            print(f"{len(options) + 1}. Done (Proceed to analysis)")
            
            try:
                choice = int(input("\nEnter your choice: "))
                if 1 <= choice <= len(options):
                    option_key = options[choice - 1]
                    if option_key in selected_keys:
                        selected_keys.remove(option_key)
                    else:
                        selected_keys.append(option_key)
                elif choice == len(options) + 1:
                    if selected_keys:
                        self.selected_symptoms = selected_keys
                        break
                    else:
                        print("Please select at least one symptom.")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")
    
    def multi_layer_questions(self):
        """Navigate through multiple layers of questions."""
        current_layer = "primary_symptoms"
        layer_count = 1
        
        for selected_symptom in self.selected_symptoms:
            layer_count += 1
            
            # Get the next layer from primary symptoms
            if selected_symptom in LAYERS["primary_symptoms"]["items"]:
                next_layer = LAYERS["primary_symptoms"]["items"][selected_symptom].get("next_layer")
                
                if next_layer and next_layer in LAYERS:
                    self.ask_layer_questions(next_layer, layer_count, selected_symptom)
    
    def ask_layer_questions(self, layer_key: str, layer_num: int, symptom_context: str):
        """Ask questions from a specific layer."""
        clear_screen()
        display_header(f"LAYER {layer_num}: {LAYERS[layer_key]['name']}")
        
        print(f"Based on your '{symptom_context.replace('_', ' ').title()}' selection:\n")
        
        layer_items = LAYERS[layer_key]["items"]
        selected_item = display_menu(
            "Please choose the most relevant option:",
            layer_items,
            show_back=False
        )
        
        # Ask follow-up questions for this layer
        if selected_item in layer_items:
            item_questions = layer_items[selected_item].get("questions", [])
            for question_key in item_questions:
                self.ask_question(question_key)
    
    def ask_question(self, question_key: str):
        """Ask a single question and record answer."""
        if question_key not in QUESTIONS:
            return
        
        question_data = QUESTIONS[question_key]
        question_text = question_data["question"]
        
        if question_data["type"] == "yes_no":
            answer = ask_yes_no_question(question_text)
            self.user_answers[question_key] = answer
        elif question_data["type"] == "multiple_choice":
            answer = ask_multiple_choice(question_text, question_data["options"])
            self.user_answers[question_key] = answer
    
    def show_results(self):
        """Display diagnosis results."""
        clear_screen()
        display_header("DIAGNOSIS RESULTS")
        
        # Calculate confidence scores
        scores = self.calculate_confidence()
        
        # Sort by confidence
        sorted_diseases = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Filter diseases with confidence > 0
        valid_diseases = [(k, v) for k, v in sorted_diseases if v > 0]
        
        if not valid_diseases:
            print("Unable to determine diagnosis from the provided information.")
            print("Please consult a healthcare professional.")
            return
        
        print("Based on your symptoms and responses, here are the likely conditions:\n")
        print("-" * 60)
        
        for rank, (disease_key, confidence) in enumerate(valid_diseases[:5], 1):
            disease = DISEASES[disease_key]
            bar_length = int(confidence / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            
            print(f"\n{rank}. {disease['name']}")
            print(f"   Confidence: {confidence:.1f}%")
            print(f"   [{bar}]")
            print(f"   Severity: {disease['severity']}")
            print(f"   Recovery Time: {disease['recovery_time']}")
            print(f"   Description: {disease['description']}")
        
        # Emergency warning
        top_disease = valid_diseases[0][0]
        if top_disease == "heart_attack":
            print("\n" + "!"*60)
            print("⚠️  CRITICAL ALERT - POSSIBLE HEART ATTACK ⚠️")
            print("CALL EMERGENCY SERVICES IMMEDIATELY!")
            print("Do not wait. Call 911 or your local emergency number.")
            print("!"*60)
        
        print("\n" + "-"*60)
        print("\nIMPORTANT REMINDERS:")
        print("• This is NOT a medical diagnosis")
        print("• Always consult with a healthcare professional")
        print("• For severe symptoms, seek immediate medical attention")
        print("• Call emergency services for life-threatening symptoms")
        
        input("\nPress Enter to continue...")


# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """Main program entry point."""
    try:
        engine = DiagnosisEngine()
        engine.start_diagnosis()
        
        # Ask if user wants to run diagnosis again
        while True:
            again = ask_yes_no_question("\nWould you like to run another diagnosis?")
            if again:
                engine = DiagnosisEngine()
                engine.start_diagnosis()
            else:
                print("\nThank you for using the Symptom Diagnosis App.")
                print("Remember to consult with a healthcare professional for proper diagnosis.")
                break
    
    except KeyboardInterrupt:
        print("\n\nApplication closed by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please try again or contact support.")


if __name__ == "__main__":
    main()
