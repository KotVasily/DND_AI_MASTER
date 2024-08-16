import asyncio
import config
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from player import Player
from master import Master
from utils import client, get_text

class DndMemory:
    def __init__(self) -> None:
        self.num_player_dict = {}
        self.players_dict = {}
        self.master_dict = {}
        self.step_history = {}
        self.system_message = {}
        self.current_player_index = {}
    
    def create_memory(self, username):
        self.num_player_dict[username] = 0 
        self.players_dict[username] = []
        self.master_dict[username] = -1
        self.current_player_index[username] = 0
        self.step_history[username] = ""
        self.system_message[username] = []

    def get_username(self, username):
        """num_player, players, master, step_history, system_message"""
        return self.num_player_dict[username], self.players_dict[username], self.master_dict[username], \
                self.step_history[username], self.system_message[username], self.current_player_index[username]
    
API_TOKEN = config.api_key_tg

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dnd_memory = DndMemory()

@dp.message(Command("start"))
async def start_game(message: types.Message):
    dnd_memory.create_memory(message.from_user.username)
    await message.reply("Добро пожаловать в игру D&D! Сколько игроков будет участвовать?")

@dp.message()
async def message_proccesing(message: types.Message):
    global dnd_memory
    username = message.from_user.username

    try:
        if dnd_memory.get_username(username)[0] == 0:
            num_player = int(message.text)
            dnd_memory.num_player_dict[message.from_user.username] = num_player
            await message.reply(f"Отлично! Создайте первого персонажа. Введите имя потом рассу через пробел. Например: Maрк Эльфы")

        else:
            if len(dnd_memory.get_username(username)[1]) != dnd_memory.get_username(username)[0]:
                name, russa = message.text.split(" ")
                player = Player(russa, name)
                dnd_memory.players_dict[username].append(player)

                await message.reply(f"Если это все персонажи напишите 'все'")
                if dnd_memory.get_username(username)[0] > 1:
                    await message.reply(f"Отлично! Создайте следущего персонажа. Введите имя потом рассу через пробел. Например: Maрк Эльфы")

            else:
                if dnd_memory.get_username(username)[2] == -1:
                    print(dnd_memory.get_username(username)[1])
                    master = Master(dnd_memory.get_username(username)[1])
                    master.generate_message_list()

                    dnd_memory.master_dict[username] = master
                    await message.reply(f"Все персонажи созданы! Сюжет: {master.plot}\n")
                    await message.reply(f'Игра начинается опишите свои действия игрок:')
                
                else:
                    if not (dnd_memory.get_username(username)[-1] != dnd_memory.get_username(username)[0]):
                        dnd_memory.system_message[username].append({
                            "role": "user",
                            "content": f'История игроков:\n{step_history}, придумай продолжения днд подробно но локанично максимум 100 слов'
                        })

                        dnd_memory.master_dict[username].messages_list_player['plot_system'] =  dnd_memory.system_message[username]
                        dnd_memory.master_dict[username].plot = get_text(dnd_memory.master_dict[username].prompt_generate_plot(), 
                                dnd_memory.system_message[username], client)
                        dnd_memory.master_dict[username].generate_message_list()

                        step_history = ""
                        dnd_memory.system_message[username] = dnd_memory.master_dict[username].messages_list_player['plot_system']
                        dnd_memory.current_player_index = 0

                    step = message.text
                    step_history = dnd_memory.get_username(username)[3]
                    player = dnd_memory.players_dict[username][dnd_memory.get_username(username)[-1]]

                    promt = f"""История игроков:\n{step_history}\n,  Игрок = {player.name}, Расса = {player.russa}, действия = {step}, кубики = {player.random_cube()},
                    Придумай для этого игрока продолжения днд подробно но локанично максимум 100 слов,
                    При этом если он разговаривает с NPC то тогда притворись этим NPC, подробности мира ты можешь узнать из истории игроков"""

                    text_model, url = dnd_memory.master_dict[username].get_step(promt, player.name)
                    dnd_memory.step_history[username] += f"Игрок = {player.name}, Расса = {player.russa}, действия = {step}\n{text_model}\n"

                    await message.answer_photo(photo=url, caption="Вот ваше изображение!")    
                    await message.reply(f"{text_model}")

                    if dnd_memory.get_username(username)[0] > 1:
                        player_name = dnd_memory.players_dict[username][dnd_memory.get_username(username)[-1]+1].name
                        dnd_memory.current_player_index[username] += 1
                        await message.reply(f'Опишите свои действия дальше игрок {player_name}:')

                    else:
                        await message.reply(f'Опишите свои действия игрок {player.name}:')

                    print(url)

    except ValueError:
        await message.reply("Введите пожалуйста цифру.")
        print()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

