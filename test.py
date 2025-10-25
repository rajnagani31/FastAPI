# demo = [{'a':1,} , {'a':2} , {'a':3}]

demo = [[1,2,3,2,2] , [1,2,3,2,2] , [1,2,3,2,2]]
print(demo)
for d in demo:
    print(list(set(d)))

"""print(list(set(demo)))""" # This give an errror demo is not work with unhashable type: 'list' ,Dictand set they work str ,int ,float ,tuple(hashable type)

set_ ={1,2}
set_.add(3)
print(set_)


dict_ = [{'a':1}]
if isinstance(dict_ , list):
    print("dict is:",dict_)
else:
    print("Some error")
print(type(dict_))


data = [1,2,3,2,2]
print(list(set(data)))


hash((1,2,3))