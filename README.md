# Baton
Baton is a simple way to do functional programming (aka. FP) in Python. It allows us to do most of FP. How much it conforms to the FP philosophy is not clear. But it does allow us to write concise and less-buggy code. I have been using in during lot of my Python work now. I have employed it at many places now and it's performing great so far.
The way to use Baton is pretty strightforward. You create a baton within your program. The baton allows you to store and get data. Whatever a function stores in the baton can be read by any other function. But no one will be able to modify it. E.g. in the code below,
```
1 baton = Baton("mybaton")
2
3 def foo(baton: Baton) -> None:
4     if not baton.peek("users"):
5         users: list = get_from_database()
6     users.append("new user")
7     baton.store("users", users)
8
9 def bar(baton: Baton) -> None:
10    users = baton.peek("users")
11    users.appand("unwanted user")
12    baton.store("users", users)
```
when function bar() tries modifying users (line 12), the baton will raise an exception.
Baton allows us to compose functions just like pipe in unix. Let's look at the code below. This code reads a request coming over network, prepares the response and then sends back the reply.
```
baton = Baton()
while baton:
    baton.push_arg("some-arg")
    baton = send_reply(
              prepare_reply(
                get_request(baton)))

    baton_name,reason,where = baton.debug()
    
```    

## Method Details
#### baton.store(key: str, value: Any, cc=True)
This function stores the given data in the baton under the name as the key. The optional argument cc (carbon copy) is by default True. Caron copy means when you read the data (using peek() method), a copy of the data is returned. If this flag is set to False, the original data (not a copy) object is returned. One use of cc being False is when the data is some unique object like queue object or fp (file pointer object).

#### baton.peek(key: str)
This function return the data stored under the key. If key is missing, it returns None. If this function is called by the same function that created the key, it returns the original data object. If a function calls this method to get data stored by another function, it returns a copy (deepcopy) of the data.

#### baton.push_arg(arg)
This method is used to pass an argument to a function. The function needs to call the pop_arg method to get the argument. A function can call it one or many times to return one or many return values.

#### baton.pop_arg()
This method is used by a function to get the argument passed to it. For every call to push_arg(), there must be a matching pop_arg().

#### baton.clean()
This method tells if the baton is clean or not. A function can mark baton as dirty if it is not returning a valid value (something went wrong). A baton marked dirty must be skipped by all functions. If a baton is dirty and a function tries calling pop_arg() to get the values passed to it, the baton will raise ValueError.

#### baton.dirty(msg="")
This method is used to mark a baton dirty. A function typically marks a baton dirty in case it sees an error or exception. Dirtying a baton is a way of telling all other functions that something worng happened in a function so they should just return quietly.
E.g.
```
def read_data(baton: Baton) -> Baton:
    try:
      data = query_db()
    except Exception:
      baton.dirty(msg="SOmething is wrong with db")
      return baton
    ....
    baton.push_arg(data)
    return baton

def process_data(baton: Baton) -> Baton:
    if not baton.clean():
        return baton
    data = baton.pop_arg()
    if not data:
        baton.dirty("Got no data!")
        return baton
     ...
     ...
 
 if __name__ == '__main__':
     baton.store("read_channel", "req-channel")
     while baton:
     
        send_data(process_data(read_data(baton)))
        
        if not baton.clean():
            _,reason,where = baton.debug()
            debug_print(where, reason)
            baton.sanitize()
```


#### baton.debug()


#### baton.sanitize()


#### baton.flush()


