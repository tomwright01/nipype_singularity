"""
Nipype interface for running a singularity container.
Example:
>>> container = SingularityTask(container="test_container/test.img",
                                args='abc')
>>> container.cmdline
singularity run test_container/test.img abc > test_singularity_log 2>&1

"""

from nipype.interfaces.base import (traits,
                                    TraitedSpec,
                                    CommandLine,
                                    CommandLineInputSpec,
                                    File)


class SingularityInputSpec(CommandLineInputSpec):
    debug = traits.Bool(usedefault=True)
    container = File(exists=True,
                     desc='Container image',
                     mandatory=True, argstr="%s", position=1)

    log_file = File(argstr="> %s 2>&1",
                    position=-1,
                    genfile=True,
                    name_source=['container'],
                    name_template='%s_singularity_log',
                    hash_files=False)


class SingularityOutputSpec(TraitedSpec):
    log_file = File(desc="Output file", exists=True)


class SingularityTask(CommandLine):
    input_spec = SingularityInputSpec
    output_spec = SingularityOutputSpec
    cmd = 'singularity run'

    def __init__(self, **inputs):
        super(SingularityTask, self).__init__(**inputs)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['log_file'] = self.inputs.log_file
        return(outputs)

if __name__ == '__main__':
    container = SingularityTask(container="test_container/test.img",
                                args='abc')
    print(container.cmdline)
    container.run()
