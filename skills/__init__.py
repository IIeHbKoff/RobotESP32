from skills.servo import ServoSkill
from skills.movement import MovementSkill
from skills.face_view import FaceViewSkill

skill_dict = {
    ServoSkill.skill_tag: ServoSkill,
    MovementSkill.skill_tag: MovementSkill,
    FaceViewSkill.skill_tag: FaceViewSkill,
}
