class Protocol:
    @staticmethod
    def prepare_packet(action: str, value) -> bytes:
        actions_dict = {
            'right_hand': 'rh',
            'left_hand': 'lh',
            'head': 'hd',
            'move_forward': 'mf',
            'move_backward': 'mb',
            'move_left': 'ml',
            'move_right': 'mr',
            'mood': 'md'
        }
        mood_dict = {
            'smile': 'smi',
            'sad': 'sad',
            'neutral': 'neu',
            'winking_left_eye': 'wle',
            'winking_right_eye': 'wre'
        }
        return f"{actions_dict[action]}:{mood_dict[value] if action == 'mood' else value}".encode()

    @staticmethod
    def parse_packet(packet: bytes) -> tuple:
        dct = {
            "rh": "right_hand",
            "lh": "left_hand",
            "hd": "head",
            'mf': 'move_forward',
            'mb': 'move_backward',
            'ml': 'move_left',
            'mr': 'move_right',
            "md": "mood",
        }
        mood_dict = {
            "smi": "smile",
            "sad": "sad",
            "neu": "neutral",
            "wle": "winking_left_eye",
            "wre": "winking_right_eye",
        }
        splitted_str = packet.decode().split(":")
        return dct.get(splitted_str[0]), mood_dict.get(splitted_str[1]) if splitted_str[0] == "md" else int(
            splitted_str[1])
