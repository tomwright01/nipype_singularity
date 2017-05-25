from .singularity import (SingularityInputSpec,
                          SingularityOutputSpec,
                          SingularityTask)
from nipype.interfaces.base import (traits,
                                    File)


class TestInputSpec(SingularityInputSpec):
    myarg = traits.Unicode(desc="An argument",
                           argstr='--myarg %s')
    dwiFile = File(argstr='--dwiFile %s',
                   desc="""Input diffusion weighted (DWI) file.""",
                   exists=True)
    returnParameterFile = File(argstr='--returnparameterfile %s',
                               desc="""Filename to write simple parameters
                               (int, float, int-vector, etc.) as opposed
                               to bulk return parameters (image, geom,
                               transform, measurement, table).""",
                               name_source=['dwiFile'],
                               hash_files=False,
                               name_template='%s_params.txt',
                               mandatory=False)


class TestOuputSpec(SingularityOutputSpec):
    returnParameterFile = File(desc="Output parameter file", exists=False)


class Test(SingularityTask):
    input_spec = TestInputSpec

    def __init__(self, **inputs):
        super(Test, self).__init__(**inputs)

    def _list_outputs(self):
        super(Test, self)._list_outputs()
        outputs = self.output_spec().get()
        outputs['returnParameterFile'] = self.inputs.log_file
        return(outputs)

if __name__ == '__main__':
    interface = Test(container='test_container/test.img',
                     dwiFile='input.nrrd')
    print(interface.cmdline)
