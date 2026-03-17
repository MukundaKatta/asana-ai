"""AsanaLibrary: Collection of 30+ yoga poses with correct joint angles."""

from __future__ import annotations

from asana.models import Asana, BreathingPattern, BreathPhase, DifficultyLevel


def _breath(phase: BreathPhase, duration: float, instruction: str) -> BreathingPattern:
    return BreathingPattern(phase=phase, duration_seconds=duration, instruction=instruction)


# ---------------------------------------------------------------------------
# Standing poses
# ---------------------------------------------------------------------------

TADASANA = Asana(
    sanskrit_name="Tadasana",
    english_name="Mountain Pose",
    description="Foundation standing pose with feet together, spine elongated, arms at sides.",
    difficulty=DifficultyLevel.BEGINNER,
    category="standing",
    target_joint_angles={
        "left_knee": 175.0, "right_knee": 175.0,
        "left_hip": 170.0, "right_hip": 170.0,
        "left_shoulder": 10.0, "right_shoulder": 10.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Improves posture", "Strengthens thighs, knees, and ankles",
              "Firms abdomen and buttocks", "Reduces flat feet"],
    hold_duration_seconds=30.0,
    breathing=[
        _breath(BreathPhase.INHALE, 4.0, "Inhale and grow tall through the crown of the head"),
        _breath(BreathPhase.EXHALE, 4.0, "Exhale and ground through the feet"),
    ],
)

VIRABHADRASANA_I = Asana(
    sanskrit_name="Virabhadrasana_I",
    english_name="Warrior I",
    description="Powerful standing lunge with arms overhead, back foot turned 45 degrees.",
    difficulty=DifficultyLevel.BEGINNER,
    category="standing",
    target_joint_angles={
        "left_knee": 90.0, "right_knee": 170.0,
        "left_hip": 90.0, "right_hip": 160.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    angle_tolerance={"left_knee": 10.0, "right_knee": 10.0},
    benefits=["Strengthens legs and arms", "Stretches hip flexors",
              "Expands chest and lungs", "Builds stamina and balance"],
    contraindications=["High blood pressure", "Heart problems"],
    hold_duration_seconds=30.0,
    breathing=[
        _breath(BreathPhase.INHALE, 4.0, "Inhale and lift arms overhead"),
        _breath(BreathPhase.EXHALE, 4.0, "Exhale and sink deeper into the front knee"),
    ],
)

VIRABHADRASANA_II = Asana(
    sanskrit_name="Virabhadrasana_II",
    english_name="Warrior II",
    description="Wide-legged stance with arms extended, front knee bent 90 degrees, gaze over front hand.",
    difficulty=DifficultyLevel.BEGINNER,
    category="standing",
    target_joint_angles={
        "left_knee": 90.0, "right_knee": 170.0,
        "left_hip": 90.0, "right_hip": 150.0,
        "left_shoulder": 90.0, "right_shoulder": 90.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
        "left_armpit": 90.0, "right_armpit": 90.0,
    },
    benefits=["Strengthens legs and ankles", "Stretches groins and inner thighs",
              "Opens hips and chest", "Builds endurance"],
    hold_duration_seconds=30.0,
)

VIRABHADRASANA_III = Asana(
    sanskrit_name="Virabhadrasana_III",
    english_name="Warrior III",
    description="Single-leg balance with torso and back leg parallel to the floor, arms forward.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="standing",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 90.0, "right_hip": 170.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Strengthens ankles and legs", "Tones abdomen",
              "Improves balance and coordination", "Strengthens back muscles"],
    hold_duration_seconds=20.0,
)

TRIKONASANA = Asana(
    sanskrit_name="Trikonasana",
    english_name="Triangle Pose",
    description="Wide stance with torso laterally extended, one hand reaching toward the floor.",
    difficulty=DifficultyLevel.BEGINNER,
    category="standing",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 120.0, "right_hip": 150.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Stretches legs, hips, and spine", "Opens chest and shoulders",
              "Strengthens thighs, knees, and ankles", "Stimulates abdominal organs"],
    hold_duration_seconds=30.0,
)

PARSVAKONASANA = Asana(
    sanskrit_name="Utthita_Parsvakonasana",
    english_name="Extended Side Angle",
    description="Front knee bent with torso extended over the front thigh, arm reaching overhead.",
    difficulty=DifficultyLevel.BEGINNER,
    category="standing",
    target_joint_angles={
        "left_knee": 90.0, "right_knee": 170.0,
        "left_hip": 90.0, "right_hip": 150.0,
        "left_shoulder": 160.0, "right_shoulder": 160.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Strengthens legs and ankles", "Stretches groins and spine",
              "Opens chest", "Stimulates abdominal organs"],
    hold_duration_seconds=30.0,
)

VRKSASANA = Asana(
    sanskrit_name="Vrksasana",
    english_name="Tree Pose",
    description="Single-leg balance with opposite foot on inner thigh, arms overhead.",
    difficulty=DifficultyLevel.BEGINNER,
    category="standing",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 45.0,
        "left_hip": 170.0, "right_hip": 90.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Improves balance", "Strengthens thighs, calves, ankles, and spine",
              "Stretches groins and inner thighs", "Calms the mind"],
    hold_duration_seconds=30.0,
)

UTKATASANA = Asana(
    sanskrit_name="Utkatasana",
    english_name="Chair Pose",
    description="Standing squat with arms reaching overhead, weight in the heels.",
    difficulty=DifficultyLevel.BEGINNER,
    category="standing",
    target_joint_angles={
        "left_knee": 110.0, "right_knee": 110.0,
        "left_hip": 110.0, "right_hip": 110.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Strengthens thighs and ankles", "Tones shoulders and arms",
              "Stretches chest and shoulders", "Stimulates heart and diaphragm"],
    hold_duration_seconds=20.0,
)

GARUDASANA = Asana(
    sanskrit_name="Garudasana",
    english_name="Eagle Pose",
    description="Single-leg balance with limbs wrapped, deep hip and shoulder stretch.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="standing",
    target_joint_angles={
        "left_knee": 120.0, "right_knee": 90.0,
        "left_hip": 120.0, "right_hip": 90.0,
        "left_shoulder": 80.0, "right_shoulder": 80.0,
        "left_elbow": 60.0, "right_elbow": 60.0,
    },
    benefits=["Strengthens calves and ankles", "Stretches shoulders and upper back",
              "Improves balance and concentration", "Opens sacroiliac joint"],
    hold_duration_seconds=20.0,
)

NATARAJASANA = Asana(
    sanskrit_name="Natarajasana",
    english_name="Dancer Pose",
    description="Standing backbend on one leg, opposite foot held behind in a deep arch.",
    difficulty=DifficultyLevel.ADVANCED,
    category="standing",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 60.0,
        "left_hip": 170.0, "right_hip": 60.0,
        "left_shoulder": 170.0, "right_shoulder": 120.0,
        "left_elbow": 170.0, "right_elbow": 90.0,
    },
    benefits=["Stretches shoulders and chest", "Strengthens legs and ankles",
              "Improves balance", "Develops grace and poise"],
    hold_duration_seconds=20.0,
)

PARIVRTTA_TRIKONASANA = Asana(
    sanskrit_name="Parivrtta_Trikonasana",
    english_name="Revolved Triangle",
    description="Triangle pose with a spinal twist, opposite hand to foot.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="standing",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 90.0, "right_hip": 160.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Stretches hamstrings and spine", "Opens chest",
              "Improves balance", "Strengthens legs"],
    hold_duration_seconds=25.0,
)

ARDHA_CHANDRASANA = Asana(
    sanskrit_name="Ardha_Chandrasana",
    english_name="Half Moon Pose",
    description="Balancing on one leg and one hand with top leg and arm extended upward.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="standing",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 90.0, "right_hip": 170.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Strengthens abdomen, ankles, thighs, buttocks, and spine",
              "Stretches groins, hamstrings, calves", "Improves coordination and balance"],
    hold_duration_seconds=20.0,
)

PRASARITA_PADOTTANASANA = Asana(
    sanskrit_name="Prasarita_Padottanasana",
    english_name="Wide-Legged Forward Bend",
    description="Wide-legged standing fold with crown of head toward the floor.",
    difficulty=DifficultyLevel.BEGINNER,
    category="standing",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 60.0, "right_hip": 60.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Stretches hamstrings and inner thighs", "Strengthens feet and legs",
              "Calms the mind", "Relieves mild backache"],
    hold_duration_seconds=30.0,
)

# ---------------------------------------------------------------------------
# Forward bends
# ---------------------------------------------------------------------------

UTTANASANA = Asana(
    sanskrit_name="Uttanasana",
    english_name="Standing Forward Bend",
    description="Standing fold with chest toward thighs, hands to floor.",
    difficulty=DifficultyLevel.BEGINNER,
    category="forward_bend",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 40.0, "right_hip": 40.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Stretches hamstrings and calves", "Strengthens thighs and knees",
              "Reduces stress and anxiety", "Stimulates liver and kidneys"],
    hold_duration_seconds=30.0,
)

PASCHIMOTTANASANA = Asana(
    sanskrit_name="Paschimottanasana",
    english_name="Seated Forward Bend",
    description="Seated fold reaching for the feet with legs extended.",
    difficulty=DifficultyLevel.BEGINNER,
    category="forward_bend",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 40.0, "right_hip": 40.0,
        "left_elbow": 140.0, "right_elbow": 140.0,
    },
    benefits=["Stretches spine, shoulders, and hamstrings",
              "Stimulates liver, kidneys, ovaries, and uterus",
              "Calms the brain", "Helps relieve stress"],
    hold_duration_seconds=45.0,
)

JANU_SIRSASANA = Asana(
    sanskrit_name="Janu_Sirsasana",
    english_name="Head-to-Knee Forward Bend",
    description="Seated forward fold with one leg extended and the other bent.",
    difficulty=DifficultyLevel.BEGINNER,
    category="forward_bend",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 45.0,
        "left_hip": 50.0, "right_hip": 90.0,
        "left_elbow": 140.0, "right_elbow": 140.0,
    },
    benefits=["Stretches spine, shoulders, hamstrings, and groins",
              "Calms the brain", "Helps relieve mild depression",
              "Stimulates liver and kidneys"],
    hold_duration_seconds=45.0,
)

# ---------------------------------------------------------------------------
# Inversions and arm balances
# ---------------------------------------------------------------------------

ADHO_MUKHA_SVANASANA = Asana(
    sanskrit_name="Adho_Mukha_Svanasana",
    english_name="Downward-Facing Dog",
    description="Inverted V-shape with hands and feet on the floor, hips lifted.",
    difficulty=DifficultyLevel.BEGINNER,
    category="inversion",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 60.0, "right_hip": 60.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Calms the brain and helps relieve stress",
              "Energizes the body", "Stretches shoulders, hamstrings, calves, and hands",
              "Strengthens arms and legs"],
    hold_duration_seconds=30.0,
    breathing=[
        _breath(BreathPhase.INHALE, 4.0, "Inhale and lengthen the spine"),
        _breath(BreathPhase.EXHALE, 4.0, "Exhale and press heels toward the floor"),
    ],
)

SIRSASANA = Asana(
    sanskrit_name="Sirsasana",
    english_name="Headstand",
    description="Full inversion balanced on the forearms and crown of the head.",
    difficulty=DifficultyLevel.ADVANCED,
    category="inversion",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 170.0, "right_hip": 170.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 90.0, "right_elbow": 90.0,
    },
    benefits=["Strengthens arms, legs, and spine", "Tones abdominal organs",
              "Improves digestion", "Calms the brain and helps relieve stress"],
    contraindications=["Back injury", "Headache", "Heart condition",
                       "High blood pressure", "Neck injury"],
    hold_duration_seconds=60.0,
)

SARVANGASANA = Asana(
    sanskrit_name="Sarvangasana",
    english_name="Shoulder Stand",
    description="Full inversion supported on the shoulders with legs vertical.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="inversion",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 170.0, "right_hip": 170.0,
        "left_elbow": 45.0, "right_elbow": 45.0,
    },
    benefits=["Calms the brain", "Stimulates thyroid and prostate glands",
              "Stretches shoulders and neck", "Tones legs and buttocks"],
    contraindications=["Neck injury", "Diarrhea", "High blood pressure"],
    hold_duration_seconds=60.0,
)

BAKASANA = Asana(
    sanskrit_name="Bakasana",
    english_name="Crow Pose",
    description="Arm balance with knees resting on upper arms, feet lifted off the floor.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="arm_balance",
    target_joint_angles={
        "left_knee": 60.0, "right_knee": 60.0,
        "left_hip": 60.0, "right_hip": 60.0,
        "left_elbow": 90.0, "right_elbow": 90.0,
        "left_shoulder": 60.0, "right_shoulder": 60.0,
    },
    benefits=["Strengthens arms and wrists", "Stretches upper back",
              "Strengthens abdominal muscles", "Opens groins"],
    hold_duration_seconds=15.0,
)

# ---------------------------------------------------------------------------
# Backbends
# ---------------------------------------------------------------------------

BHUJANGASANA = Asana(
    sanskrit_name="Bhujangasana",
    english_name="Cobra Pose",
    description="Prone backbend with chest lifted, hands under shoulders, elbows slightly bent.",
    difficulty=DifficultyLevel.BEGINNER,
    category="backbend",
    target_joint_angles={
        "left_elbow": 140.0, "right_elbow": 140.0,
        "left_shoulder": 40.0, "right_shoulder": 40.0,
        "left_hip": 160.0, "right_hip": 160.0,
        "left_knee": 170.0, "right_knee": 170.0,
    },
    benefits=["Strengthens the spine", "Stretches chest, lungs, shoulders, and abdomen",
              "Firms the buttocks", "Opens the heart"],
    contraindications=["Back injury", "Pregnancy"],
    hold_duration_seconds=20.0,
)

URDHVA_MUKHA_SVANASANA = Asana(
    sanskrit_name="Urdhva_Mukha_Svanasana",
    english_name="Upward-Facing Dog",
    description="Prone backbend with arms straight, thighs lifted off the floor.",
    difficulty=DifficultyLevel.BEGINNER,
    category="backbend",
    target_joint_angles={
        "left_elbow": 170.0, "right_elbow": 170.0,
        "left_shoulder": 50.0, "right_shoulder": 50.0,
        "left_hip": 170.0, "right_hip": 170.0,
        "left_knee": 170.0, "right_knee": 170.0,
    },
    benefits=["Improves posture", "Strengthens spine, arms, and wrists",
              "Stretches chest, lungs, shoulders, and abdomen", "Firms the buttocks"],
    hold_duration_seconds=15.0,
)

USTRASANA = Asana(
    sanskrit_name="Ustrasana",
    english_name="Camel Pose",
    description="Kneeling backbend reaching hands to heels, chest open.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="backbend",
    target_joint_angles={
        "left_knee": 90.0, "right_knee": 90.0,
        "left_hip": 150.0, "right_hip": 150.0,
        "left_shoulder": 130.0, "right_shoulder": 130.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Stretches the front of the body", "Strengthens back muscles",
              "Opens chest and hip flexors", "Stimulates abdominal organs"],
    hold_duration_seconds=20.0,
)

DHANURASANA = Asana(
    sanskrit_name="Dhanurasana",
    english_name="Bow Pose",
    description="Prone backbend holding ankles, body shaped like a bow.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="backbend",
    target_joint_angles={
        "left_knee": 60.0, "right_knee": 60.0,
        "left_hip": 150.0, "right_hip": 150.0,
        "left_shoulder": 120.0, "right_shoulder": 120.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Stretches the entire front of the body",
              "Strengthens back muscles", "Improves posture",
              "Stimulates abdominal organs"],
    hold_duration_seconds=20.0,
)

SETU_BANDHASANA = Asana(
    sanskrit_name="Setu_Bandhasana",
    english_name="Bridge Pose",
    description="Supine backbend with feet on the floor and hips lifted.",
    difficulty=DifficultyLevel.BEGINNER,
    category="backbend",
    target_joint_angles={
        "left_knee": 90.0, "right_knee": 90.0,
        "left_hip": 160.0, "right_hip": 160.0,
        "left_shoulder": 10.0, "right_shoulder": 10.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Stretches chest, neck, and spine", "Calms the brain",
              "Reduces anxiety and stress", "Strengthens legs and buttocks"],
    hold_duration_seconds=30.0,
)

URDHVA_DHANURASANA = Asana(
    sanskrit_name="Urdhva_Dhanurasana",
    english_name="Wheel Pose",
    description="Full backbend with hands and feet on the floor, hips and chest lifted.",
    difficulty=DifficultyLevel.ADVANCED,
    category="backbend",
    target_joint_angles={
        "left_knee": 90.0, "right_knee": 90.0,
        "left_hip": 160.0, "right_hip": 160.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Strengthens arms, wrists, legs, buttocks, abdomen, and spine",
              "Stretches chest and lungs", "Stimulates thyroid and pituitary",
              "Increases energy and counteracts depression"],
    contraindications=["Back injury", "Carpal tunnel", "Heart problems"],
    hold_duration_seconds=15.0,
)

# ---------------------------------------------------------------------------
# Seated and hip openers
# ---------------------------------------------------------------------------

PADMASANA = Asana(
    sanskrit_name="Padmasana",
    english_name="Lotus Pose",
    description="Classic seated meditation pose with legs crossed and feet on opposite thighs.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="seated",
    target_joint_angles={
        "left_knee": 30.0, "right_knee": 30.0,
        "left_hip": 60.0, "right_hip": 60.0,
    },
    benefits=["Calms the mind", "Stimulates pelvis, spine, abdomen, and bladder",
              "Stretches ankles and knees", "Eases menstrual discomfort"],
    contraindications=["Ankle injury", "Knee injury"],
    hold_duration_seconds=120.0,
)

BADDHA_KONASANA = Asana(
    sanskrit_name="Baddha_Konasana",
    english_name="Bound Angle Pose",
    description="Seated with soles of feet together, knees dropping toward the floor.",
    difficulty=DifficultyLevel.BEGINNER,
    category="seated",
    target_joint_angles={
        "left_knee": 60.0, "right_knee": 60.0,
        "left_hip": 80.0, "right_hip": 80.0,
    },
    benefits=["Stretches inner thighs, groins, and knees",
              "Stimulates abdominal organs and heart",
              "Improves circulation", "Helps relieve mild depression and anxiety"],
    hold_duration_seconds=60.0,
)

GOMUKHASANA = Asana(
    sanskrit_name="Gomukhasana",
    english_name="Cow Face Pose",
    description="Seated with stacked knees and arms clasped behind the back.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="seated",
    target_joint_angles={
        "left_knee": 45.0, "right_knee": 45.0,
        "left_shoulder": 170.0, "right_shoulder": 40.0,
        "left_elbow": 90.0, "right_elbow": 90.0,
    },
    benefits=["Stretches ankles, hips, thighs, shoulders, chest, and triceps",
              "Helps with chronic knee pain", "Decompresses lower spine"],
    hold_duration_seconds=30.0,
)

ARDHA_MATSYENDRASANA = Asana(
    sanskrit_name="Ardha_Matsyendrasana",
    english_name="Half Lord of the Fishes",
    description="Seated twist with one leg bent and the opposite arm wrapping the knee.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="seated",
    target_joint_angles={
        "left_knee": 90.0, "right_knee": 45.0,
        "left_hip": 90.0, "right_hip": 90.0,
        "left_elbow": 90.0, "right_elbow": 90.0,
    },
    benefits=["Energizes the spine", "Stretches shoulders, hips, and neck",
              "Stimulates digestive fire", "Relieves backache and sciatica"],
    hold_duration_seconds=30.0,
)

NAVASANA = Asana(
    sanskrit_name="Navasana",
    english_name="Boat Pose",
    description="Balancing on sit bones with legs and torso lifted to form a V shape.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="seated",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 70.0, "right_hip": 70.0,
        "left_shoulder": 70.0, "right_shoulder": 70.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Strengthens abdomen, hip flexors, and spine",
              "Stimulates kidneys, thyroid, and intestines",
              "Improves digestion", "Builds core strength"],
    hold_duration_seconds=20.0,
)

# ---------------------------------------------------------------------------
# Supine poses
# ---------------------------------------------------------------------------

SAVASANA = Asana(
    sanskrit_name="Savasana",
    english_name="Corpse Pose",
    description="Supine relaxation with arms and legs extended, palms facing up.",
    difficulty=DifficultyLevel.BEGINNER,
    category="supine",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 170.0, "right_hip": 170.0,
        "left_shoulder": 30.0, "right_shoulder": 30.0,
        "left_elbow": 160.0, "right_elbow": 160.0,
    },
    benefits=["Relaxes the whole body", "Reduces headache, fatigue, and insomnia",
              "Helps lower blood pressure", "Calms the mind"],
    hold_duration_seconds=300.0,
    breathing=[
        _breath(BreathPhase.NATURAL, 300.0, "Breathe naturally; let go of all effort"),
    ],
)

SUPTA_BADDHA_KONASANA = Asana(
    sanskrit_name="Supta_Baddha_Konasana",
    english_name="Reclining Bound Angle Pose",
    description="Supine with soles of feet together and knees open to the sides.",
    difficulty=DifficultyLevel.BEGINNER,
    category="supine",
    target_joint_angles={
        "left_knee": 60.0, "right_knee": 60.0,
        "left_hip": 80.0, "right_hip": 80.0,
        "left_shoulder": 30.0, "right_shoulder": 30.0,
        "left_elbow": 150.0, "right_elbow": 150.0,
    },
    benefits=["Opens hips and groins", "Stretches inner thighs",
              "Calms the nervous system", "Relieves mild depression"],
    hold_duration_seconds=120.0,
)

HALASANA = Asana(
    sanskrit_name="Halasana",
    english_name="Plow Pose",
    description="Supine inversion with legs overhead and toes touching the floor behind the head.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="supine",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 30.0, "right_hip": 30.0,
        "left_shoulder": 10.0, "right_shoulder": 10.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Calms the brain", "Stimulates abdominal organs and thyroid",
              "Stretches shoulders and spine", "Therapeutic for backache and headache"],
    contraindications=["Neck injury", "Pregnancy", "Diarrhea"],
    hold_duration_seconds=30.0,
)

# ---------------------------------------------------------------------------
# Plank and core
# ---------------------------------------------------------------------------

CHATURANGA_DANDASANA = Asana(
    sanskrit_name="Chaturanga_Dandasana",
    english_name="Four-Limbed Staff Pose",
    description="Low plank with elbows bent at 90 degrees, body hovering above the floor.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="core",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 170.0, "right_hip": 170.0,
        "left_elbow": 90.0, "right_elbow": 90.0,
        "left_shoulder": 45.0, "right_shoulder": 45.0,
    },
    benefits=["Strengthens arms and wrists", "Tones the abdomen",
              "Prepares for arm balances", "Builds upper body strength"],
    hold_duration_seconds=10.0,
)

VASISTHASANA = Asana(
    sanskrit_name="Vasisthasana",
    english_name="Side Plank Pose",
    description="Side plank balanced on one arm and the side of one foot.",
    difficulty=DifficultyLevel.INTERMEDIATE,
    category="core",
    target_joint_angles={
        "left_knee": 170.0, "right_knee": 170.0,
        "left_hip": 170.0, "right_hip": 170.0,
        "left_shoulder": 170.0, "right_shoulder": 170.0,
        "left_elbow": 170.0, "right_elbow": 170.0,
    },
    benefits=["Strengthens arms, belly, and legs",
              "Stretches and strengthens wrists",
              "Improves balance", "Strengthens core"],
    hold_duration_seconds=15.0,
)


class AsanaLibrary:
    """Central catalog of all supported yoga asanas.

    Provides lookup by Sanskrit name, English name, difficulty, or category.
    Ships with 30+ traditional asanas.
    """

    def __init__(self) -> None:
        self._asanas: dict[str, Asana] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Load all built-in asana definitions."""
        defaults = [
            TADASANA, VIRABHADRASANA_I, VIRABHADRASANA_II, VIRABHADRASANA_III,
            TRIKONASANA, PARSVAKONASANA, VRKSASANA, UTKATASANA,
            GARUDASANA, NATARAJASANA, PARIVRTTA_TRIKONASANA, ARDHA_CHANDRASANA,
            PRASARITA_PADOTTANASANA,
            UTTANASANA, PASCHIMOTTANASANA, JANU_SIRSASANA,
            ADHO_MUKHA_SVANASANA, SIRSASANA, SARVANGASANA, BAKASANA,
            BHUJANGASANA, URDHVA_MUKHA_SVANASANA, USTRASANA, DHANURASANA,
            SETU_BANDHASANA, URDHVA_DHANURASANA,
            PADMASANA, BADDHA_KONASANA, GOMUKHASANA, ARDHA_MATSYENDRASANA, NAVASANA,
            SAVASANA, SUPTA_BADDHA_KONASANA, HALASANA,
            CHATURANGA_DANDASANA, VASISTHASANA,
        ]
        for asana in defaults:
            self._asanas[asana.sanskrit_name] = asana

    def get(self, sanskrit_name: str) -> Asana | None:
        """Look up an asana by its Sanskrit name."""
        return self._asanas.get(sanskrit_name)

    def get_by_english(self, english_name: str) -> Asana | None:
        """Look up an asana by its English name (case-insensitive)."""
        target = english_name.lower()
        for asana in self._asanas.values():
            if asana.english_name.lower() == target:
                return asana
        return None

    def list_all(self) -> list[Asana]:
        """Return all asanas sorted alphabetically by Sanskrit name."""
        return sorted(self._asanas.values(), key=lambda a: a.sanskrit_name)

    def filter_by_difficulty(self, difficulty: DifficultyLevel) -> list[Asana]:
        """Return asanas matching the given difficulty level."""
        return [a for a in self._asanas.values() if a.difficulty == difficulty]

    def filter_by_category(self, category: str) -> list[Asana]:
        """Return asanas matching the given category."""
        return [a for a in self._asanas.values() if a.category == category]

    def search(self, query: str) -> list[Asana]:
        """Search asanas by partial name match (case-insensitive)."""
        q = query.lower()
        results = []
        for asana in self._asanas.values():
            if q in asana.sanskrit_name.lower() or q in asana.english_name.lower():
                results.append(asana)
        return results

    def add(self, asana: Asana) -> None:
        """Add a custom asana to the library."""
        self._asanas[asana.sanskrit_name] = asana

    @property
    def count(self) -> int:
        """Return the total number of asanas in the library."""
        return len(self._asanas)
