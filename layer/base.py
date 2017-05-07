import tensorflow as tf


class Layer(object):
    def __init__(self, name='untitled_op'):
        self._op = tf.make_template(name, self.layer_op, create_scope_now_=True)

    def layer_op(self, *args, **kwargs):
        msg = 'method \'layer_op\' in \'{}\''.format(type(self).__name__)
        raise NotImplementedError(msg)

    def __call__(self, *args, **kwargs):
        return self._op(*args, **kwargs)

    def __str__(self):
        return self.to_string()

    def layer_scope(self):
        return self._op.variable_scope

    def trainable_variables(self):
        return tf.get_collection(
                tf.GraphKeys.TRAINABLE_VARIABLES,
                self.layer_scope().name)

    def to_string(self):
        layer_scope_name = self.layer_scope().name
        out_str = "\033[42m[Layer]\033[0m {}".format(layer_scope_name)
        if not self._op._variables_created:
            out_str += ' \033[46m(input undecided)\033[0m'
            return out_str
        layer_variables = self.trainable_variables()
        if len(layer_variables) ==0:
            out_str += ' (not trainable)'
            return out_str
        out_str += ' \033[92m[Trainable]\033[0m '
        out_str += ', '.join([v.name.split(':')[0][len(layer_scope_name)+1:]
            for v in layer_variables])
        return out_str
