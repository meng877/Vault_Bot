from mcdreforged.api.all import *
import time

class Config(Serializable):
    bot_prefix: str = 'bot_'  #假人前缀
    wait_time: int = 5  #等待时长(秒)


@new_thread
def vault_start(source: CommandSource, content: CommandContext):
    server = source.get_server()
    name = content['name']
    source.reply(f"假人组{name}任务开始")
    tasklist[name] = 0
    server.execute(f'execute at {str(source)[7:]} run player vault_{name} spawn')
    server.execute(f'gamemode spectator {config.bot_prefix}vault_{name}')
    time.sleep(10)
    for i in range(1,129):
        if tasklist[name] == -1:
            break
        server.execute(f'execute at {config.bot_prefix}vault_{name} run player vault_{name}_{i} spawn')
        time.sleep(config.wait_time)
        server.execute(f'gamemode survival {config.bot_prefix}vault_{name}_{i}')
        server.execute(f'player {config.bot_prefix}vault_{name}_{i} use once')
        time.sleep(1)
        server.execute(f'player {config.bot_prefix}vault_{name}_{i} kill')
        time.sleep(1)
    server.execute(f'player {config.bot_prefix}vault_{name} kill')
    source.reply(f"假人组{name}任务结束，共生成{i}次")

def vault_stop(source: CommandSource, content: CommandContext):
    try:
        if tasklist[content['name']] != -1:
            tasklist[content['name']] = -1
    except KeyError:
        source.reply(f"没有找到任务 {content['name']}")


def vault_stop_all(source: CommandSource, content: CommandContext):
    for name in tasklist:
        tasklist[name] = -1
    source.reply("所有任务均已停止")

def show_tasklist(source: CommandSource, content: CommandContext):
    for name in tasklist():
        message += f"任务{name}：生成次数：{tasklist[name]}"
    source.reply(message)

def on_load(server: PluginServerInterface, prev_module):
    global config, tasklist
    tasklist = {}
    config = server.load_config_simple(target_class=Config)
    builder = SimpleCommandBuilder()
    builder.command('!!vault start <name>', vault_start)
    builder.command('!!vault stop <name>', vault_stop)
    builder.command('!!vault stop all', vault_stop_all)
    builder.command('!!vault task', show_tasklist)
    builder.arg('name', Text)
    builder.register(server)

def on_unload(server: PluginServerInterface):
    vault_stop_all()
