class Error(Exception):
    pass


class CreationError(Error):
    def __init__(self, obj_type, obj_name, cft_prop, cft_value, err):
        self.object = {
            'type': obj_type,
            'name': obj_name
        }
        self.conflict = {
            'type': cft_prop,
            'property': cft_value
        }
        self.message = self.generate_message(err)

    def generate_message(self, err):
        switcher = {
            'Exists': 'A {} with the {} `{}` already exists!'.format(
                self.object['type'],
                self.conflict['property'],
                self.conflict['value']),
            'Installed': 'The {} {} is already present on the {} {}'.format(
                self.conflict['property'],
                self.conflict['value'],
                self.object['type'],
                self.object['name'])
        }

        return switcher.get(err, err)


class LoadError(Error):
    def __init__(self, obj_type, obj_name, err):
        self.object = {
            'type': obj_type,
            'name': obj_name
        }
        self.type = err
        self.message = self.generate_message()

    def generate_message(self):
        switcher = {
            'NotExist': 'The {} `{}` doesn\'t exist!'.format(
                self.object['type'],
                self.object['name']),
            'NoContext': ('No cluster specified nor managed! Use "--cluster" '
                          'to specify a cluster.'),
            'MustExit': ('You are currently managing the cluster `{}`. '
                         'Type "exit" to manage other clusters.'.format(
                             self.object['name'])),
            'NoConfFile': ('Couldn\'t find the file `jumbo_config` for cluster'
                           ' `{}`\nAll cluster configuration has been lost.'
                           .format(self.object['name']))
        }
        return switcher.get(self.type, self.type)
