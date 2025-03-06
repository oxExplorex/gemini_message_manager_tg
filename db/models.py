from tortoise.models import Model
from tortoise import fields


# до фикса ошибочки пусть будет null=True | не должно по пизде все идти :)

class username_history_db(Model):
    """

    База данных юзернеймов (Грубо говоря история юзеров)

    """
    uuid = fields.UUIDField(pk=True)

    user_id = fields.BigIntField(unique=True, null=True)
    username = fields.TextField(default=None, null=True)

    date = fields.BigIntField()



class user_db(Model):
    """

    База данных пользователей

    """
    uuid = fields.UUIDField(pk=True)
    user_id = fields.BigIntField(unique=True)

    username = fields.TextField(default=None, null=True)  # Актуальный юзер
    full_name = fields.TextField(default=None, null=True)

    roles = fields.TextField(default=None, null=True)  # может ли пользоваться ботом :)



class app_tg_db(Model):
    uuid = fields.UUIDField(pk=True)

    user_id = fields.BigIntField(null=True)

    app_id = fields.BigIntField(null=True)
    api_hash = fields.TextField(null=True)

    tag_name = fields.TextField(default="No Name", null=True)



class apps_db(Model):
    uuid = fields.UUIDField(pk=True)
    admin_id = fields.BigIntField(null=True)

    # user_id TG
    user_id = fields.BigIntField(default=None, null=True)

    app_tg = fields.UUIDField(default=None, null=True)
    number = fields.TextField(default=None, null=True)

    # todo: нужно ли сохранять файлы временные ()
    # downloads_temp_file = fields.SmallIntField(default=1, null=True)

    # todo: Нужно ли оповещать о черном списке
    alert_black_list = fields.SmallIntField(default=1, null=True)
    alert_black_list_id = fields.BigIntField(default=1, null=True)

    # Нужно ли оповещать об удаленных чатах
    alert_del_chat = fields.SmallIntField(default=1, null=True)
    alert_del_chat_id = fields.BigIntField(default=1, null=True)

    # Нужно ли оповещать о новых чатах
    alert_new_chat = fields.SmallIntField(default=1, null=True)
    alert_new_chat_id = fields.BigIntField(default=1, null=True)

    # оповещения о ботах / каналах
    alert_bot = fields.SmallIntField(default=1, null=True)

    # Каждый апдейт будет сохраняться, чтобы видеть что все воркает
    last_update = fields.BigIntField(default=None, null=True)


class history_users_db(Model):
    # логи действий
    uuid = fields.UUIDField(pk=True)

    # id основы
    admin_id = fields.BigIntField()

    # id таргета
    user_id = fields.BigIntField()

    # action id
    # Действие, которое было совершено
    action_id = fields.SmallIntField()

    # дата
    date = fields.BigIntField()


class dump_chat_user_db(Model):
    # База данных чатов, которые есть на данный момент
    uuid = fields.UUIDField(pk=True)

    admin_id = fields.BigIntField()
    chat_id = fields.BigIntField()











