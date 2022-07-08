from run import db, Users


def create_users(count):

    users = []
    for i in range(count):
        name = 'user' + str(i)
        user = Users(name=f'{name}')
        users.append(user)

    for u in users:
        db.session.add(u)

    db.session.commit()


create_users(10)

