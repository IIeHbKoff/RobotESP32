from skills import skill_dict


class Protocol:
    start_end_symbol = "&"
    tags_delimiter = ";"
    tag_value_delimiter = ":"

    def prepare_packet(self, skills: list) -> bytes:
        data_string = f"{self.tags_delimiter}".join(skills)
        return f"{self.start_end_symbol}{data_string}{self.start_end_symbol}".encode()

    def parse_packet(self, packet: bytes) -> list:
        packets: list = packet.decode().replace(self.start_end_symbol, "").split(self.tags_delimiter)
        answer = list()
        for pack in packets:
            split_pack = tuple(pack.split(self.tag_value_delimiter))
            answer.append((skill_dict.get(split_pack[0]), split_pack[1]))
        return answer
