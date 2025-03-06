from tortoise import Tortoise

from data.config import user, password, host, db, port, db_http, admin_id_list
from db.models import user_db, app_tg_db, apps_db, dump_chat_user_db

TORTOISE_ORM = {
    "connections": {"default": f'{db_http}://{user}:{password}@{host}:{port}/{db}'},
    "apps": {
        "models": {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

async def connect_database():
    await Tortoise.init(TORTOISE_ORM)


async def close_database():
    await Tortoise.close_connections()

##############################################
##############################################

async def get_user(user_id):
    return await user_db.filter(user_id=user_id).first()

async def update_user(user_id, username, full_name):
    _temp = await user_db.filter(user_id=user_id).first()
    _roles = "admin" if user_id in admin_id_list else None
    if not _temp:
        _temp = await user_db.create(
            user_id=user_id,
            roles=_roles,
        )

    if _temp.roles != _roles or _temp.username != username or _temp.full_name != full_name:
        await _temp.update_from_dict({
            "username": username,
            "full_name": full_name,
            "roles": _roles,
        })
        await _temp.save()


async def delete_user(user_id):
    _temp = await user_db.filter(user_id=user_id).first()
    if _temp:
        await _temp.delete()
        await _temp.save()


async def get_admins():
    return await user_db.filter(roles="admin").all()

##############################################
##############################################

async def get_app_tg_user_id(user_id, offset=0):
    return (
        await app_tg_db.filter(user_id=user_id).offset(offset).limit(5),
        await app_tg_db.filter(user_id=user_id).count(),
    )


async def get_app_tg_uuid(uuid, user_id):
    return await app_tg_db.filter(uuid=uuid, user_id=user_id).first()

async def get_app_tg_uuid_aio(uuid):
    return await app_tg_db.filter(uuid=uuid).first()

async def del_app_tg_uuid(uuid, user_id):
    _temp = await app_tg_db.filter(uuid=uuid, user_id=user_id).first()
    if _temp:
        await _temp.delete()
        await _temp.save()
        return True
    return False



async def get_app_tg_to_params_all(user_id, app_id, api_hash):
    return await app_tg_db.filter(user_id=user_id, app_id=app_id, api_hash=api_hash).first()

async def create_app_tg(user_id, app_id, api_hash, tag_name):
    await app_tg_db.create(
        user_id=user_id,
        app_id=app_id,
        api_hash=api_hash,
        tag_name=tag_name,
    )


##############################################
##############################################

async def get_account_user_id(admin_id, offset=0):
    return (
        await apps_db.filter(admin_id=admin_id).offset(offset).limit(5),
        await apps_db.filter(admin_id=admin_id).count(),
    )


async def get_account_all():
    return await apps_db.filter().all()


async def get_account_tg_to_user_id(user_id):
    return await apps_db.filter(user_id=user_id).first()

async def get_account_uuid(uuid, admin_id):
    return await apps_db.filter(uuid=uuid, admin_id=admin_id).first()

async def del_account_uuid(uuid, admin_id):
    _temp = await apps_db.filter(uuid=uuid, admin_id=admin_id).first()
    if _temp:
        await _temp.delete()
        await _temp.save()
        return True
    return False


async def create_account_tg(admin_id, user_id, app_tg, number):
    await apps_db.create(
        admin_id=admin_id,
        user_id=user_id,
        app_tg=app_tg,
        number=number,

        alert_del_chat_id=admin_id,
        alert_new_chat_id=admin_id,

    )


##############################################
##############################################
async def get_dump_chat_admin_all(admin_id):
    return await dump_chat_user_db.filter(admin_id=admin_id).all()

async def get_dump_chat_user(admin_id, chat_id):
    return await dump_chat_user_db.filter(admin_id=admin_id, chat_id=chat_id).first()


async def del_dump_chat_user(admin_id, chat_id):
    _temp = await dump_chat_user_db.filter(admin_id=admin_id, chat_id=chat_id).all()
    if _temp:
        for i in _temp:
            await i.delete()
            await i.save()
        return True
    return False


async def create_dump_chat_user(admin_id, chat_id):
    await dump_chat_user_db.create(
        admin_id=admin_id,
        chat_id=chat_id,
    )
