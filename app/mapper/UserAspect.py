import UserIdMap
import UserMapper


def wrap_find(func, map_object):
    def new_find(userId):
        user = map_object.find(int(userId))
        if user is not None:
            print(map_object.__name__ + ' - Cache HIT')
            return user
        print(map_object.__name__ + ' - Cache MISS')
        result = func(userId)
        if not result:
            return
        else:
            map_object.addTo(result)
        return result
    return new_find

UserMapper.find = wrap_find(UserMapper.find, UserIdMap)

print('attached aspect successfully')
