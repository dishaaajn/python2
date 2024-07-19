from mongodb3 import mongodb_helper
from mongodb2 import users
from bson.objectid import ObjectId
from tabulate import tabulate


def main ():
    print("Welcome to Doctor's App")
    db_helper = mongodb_helper()
    # #insert user
    # user = users()
    # user.add_user_detail()    
    # db_helper.insert(vars(user))
    # print('insert done')
    # print("===================================")

    #fetching all users
    all_users=db_helper.fetch()
    headers = list(all_users[0].keys())
    print(headers)
    print(tabulate(all_users,tablefmt='grid'))
    print("===================================")

    #update user
    query = {'name':'disha' , 'gender' : 'female'}
    document_to_update = {'email' : 'disha123@gmail.com'}
    db_helper.update(document_to_update,query)
    print('update done')
    print("===================================")
       
    #fetching using traits
    query = {'name':'disha'}
    print(db_helper.fetch(query))
    print('fetching using traits done')
    print("===================================")

    #fetchting using object id
    query = {'_id' : ObjectId('6693780e1c54ede4ecc65fce')}
    print(db_helper.fetch(query))
    print('fetching using object id done')
    print("===================================")

    #delete '6693780e1c54ede4ecc65fce'
    query={'name' : 'disha'}
    db_helper.delete(query)
    print('delete done')
    print("===================================")


if __name__ == "__main__":
    main()