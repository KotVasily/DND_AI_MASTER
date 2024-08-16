import config
from openai import OpenAI
from utils import get_text, get_image, client

class Master:
    def __init__(self, player_list) -> None:
        """
        plot = сюжет
        client = нужен для g4f
        players = список игроков
        messages_list = сообщения для мастера
        """
        self.messages_list_player = {}
        self.messages_list_player['plot_system'] = []
        self.player_list = player_list
        self.promt_plot = """Сгенерируй сюжет для игры Подземелья и Драконы на основе персонажей
        , также напиши о началньой локации начальной максимально максимально 
        подробно(этот промт попадет другим gpt которые бдут генерировать новые ходы, когда все игроки сделают по ходу ты сгенерируешь продолжения
          на основе всех ходов игроков)
          Игроки: """ 
        self.plot = get_text(self.prompt_generate_plot(), [], client)

    def generate_message_list(self):
        for player in self.player_list:
            print(player.name)
            self.messages_list_player[player.name] = []
            self.messages_list_player[player.name].append({
                "role": "user",
                "content": self.plot
            })

        self.messages_list_player['plot_system'].append({
                "role": "user",
                "content": self.plot
            })

    def prompt_generate_plot(self):
        return self.promt_plot + ", ".join(f"Имя = {player.name}, Расса = {player.russa}" for player in self.player_list)
    
    def get_player_index(self, player_name):
        index_player = 0

        for i, player in enumerate(self.player_list):
            if player.name == player_name:
                index_player = i
                break

        return int(index_player)
    
    def get_step(self, voice, player_name):
        print(self.messages_list_player)
        text = get_text(voice, self.messages_list_player[player_name], client)
        text_generate_image = get_text(
                 "Максимально опиши что происходить вокруг это промт для создания изоображения, просто верни промт без всего только промт, но у тебя всего 10 слов на англиском языке используй только буквы",
                 self.messages_list_player[player_name], client, save_message=False)
        
        print(text_generate_image)
        url_image = get_image(text_generate_image, client)

        return text, url_image

