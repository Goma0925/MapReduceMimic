import pkgutil

def get_all_default_modules():
    modules = []

    for module in pkgutil.iter_modules():
        print("LOOP:", module)
        modules.append(str(module.name))
        print(str(module.name))

get_all_default_modules()