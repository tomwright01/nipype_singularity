from .singularity import (SingularityInputSpec,
                          SingularityTask,
                          SingularityFile)
from nipype.interfaces.base import (traits,
                                    TraitedSpec,
                                    File)


class TestInputSpec(SingularityInputSpec):
    myarg = traits.Unicode(desc="An argument",
                           argstr='--myarg %s')
    dwiFile = SingularityFile(argstr='--dwiFile %s',
                              desc="Input diffusion weighted (DWI) file.",
                              container_path='/input',
                              exists=True)
    # returnParameterFile = File(argstr='--returnparameterfile %s',
    #                            desc="""Filename to write simple parameters
    #                            (int, float, int-vector, etc.) as opposed
    #                            to bulk return parameters (image, geom,
    #                            transform, measurement, table).""",
    #                            name_source=['dwiFile'],
    #                            hash_files=False,
    #                            name_template='%s_params.txt',
    #                            mandatory=False)
    returnParameterFile = traits.Bool(desc="Write a return parameter file.",
                                      usedefault=True)
    returnParameterFileName = File(requires=['returnParameterFile'],
                                   argstr='--returnparameterfile %s',
                                   desc=("Filename to write simple parameters "
                                         "(int, float, int-vector, etc.) "
                                         "as opposed to bulk return parameters"
                                         "(image, geom, transform, measurement"
                                         ", table)."),
                                   name_source=['dwiFile'],
                                   hash_files=False,
                                   name_template='%s_params.txt')

    inputSubject = File(argstr="%s",
                        position=1,
                        desc=("One subject data: "
                              "whole-brain tractography as vtkPoly data "
                              "(.vtk or .vtp)"))


class TestOuputSpec(TraitedSpec):
    returnParameterFile = File(desc="Output parameter file", exists=False)


class Test(SingularityTask):
    container_cmd = 'mycmd'
    input_spec = TestInputSpec

    def _list_outputs(self):
        super(Test, self)._list_outputs()
        outputs = self.output_spec().get()
        outputs['returnParameterFile'] = self.inputs.log_file
        return(outputs)

    def _parse_inputs(self):
        if not self.inputs.returnParameterFile:
            self.inputs.trait("returnParameterFileName").argstr = None
        return super(Test, self)._parse_inputs()
