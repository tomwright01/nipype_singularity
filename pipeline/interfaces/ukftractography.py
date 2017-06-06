"""
Nipype interface for Unscented Kalman Tractography (ukftractography)
"""

from .singularity import (SingularityInputSpec,
                          SingularityTask,
                          SingularityFile)
from nipype.interfaces.base import (traits,
                                    TraitedSpec,
                                    File)

from nipype.external.due import BibTeX


class UKFTractographyInputSpec(SingularityInputSpec):
    returnParameterFile = SingularityFile(argstr='--returnparameterfile %s',
                                          desc=("Filename to write simple "
                                                "parameters (int, float, "
                                                "int-vector, etc.) as opposed "
                                                "to bulk return parameters "
                                                "(image, geom, transform, "
                                                "measurement, table)."),
                                          name_source=['dwiFile'],
                                          hash_files=False,
                                          name_template='%s_params.txt')

    xml = traits.Bool(argstr='--xml',
                      desc="Produce the xml description of cmdline args")

    echo = traits.Bool(argstr='--echo',
                       desc="Echo the command line arguments")

    sigmaSignal = traits.Float(argstr='--sigmaSignal %f',
                               desc="""UKF Data Term: Sigma for Gaussian kernel
                               used to interpolate the signal at sub-voxel
                               locations. Default 0.0""")
    rs = traits.Float(argstr='--Rs %f',
                      desc=""" UKF Data Term:
                      Measures expected noise in signal.
                      This is used by the UKF method to decide how much to
                      trust the data. This should be increased for very noisy
                      data or reduced for high quality data.
                      Defaults: single tensor/orientation-0.01; other-0.02.
                      Suggested Range: 0.001-0.25.
                      Default of 0.0 indicates the program will assign value
                      based on other model parameters. (default: 0))""")
    qvic = traits.Float(argstr="--Qvic %f",
                        desc="""UKF data fitting parameter for NODDI model
                        Rate of change of volume fraction of intracellular
                        component.
                        Default: 0.004. (default: 0.004))""")
    qkappa = traits.Float(argstr="--Qkappa %f",
                          desc="""UKF data fitting parameter for NODDI model:
                          Rate of change of kappa (orientation dispersion)
                          value.
                          Higher kappa values indicate more fiber dispersion.
                          Default: 0.01. (default: 0.01)""")
    recordViso = traits.Bool(argstr='--recordViso',
                             desc="""Record output from NODDI model:
                             Store volume fraction of CSF compartment
                             along fibers""")
    recordKappa = traits.Bool(argstr='--recordKappa',
                              desc="""Record output from NODDI model:
                              concentration parameter that measures the extent
                              of orientation dispaersion.""")
    recordVic = traits.Bool(argstr='--recordVic',
                            desc="""Record output from NODDI model:
                            Store volume fraction of intra-cellular compartment
                            along fibers""")
    useNoddi = traits.Bool(argstr='--noddi',
                           desc="""Use neurite orientation dispersion and
                           density imaging (NODDI) model instead of
                           tensor model.""",)
    qw = traits.Float(argstr='--Qw %f',
                      desc="""UKF data fitting parameter for tensor plus
                      free water model:
                      Process noise for free water weights,
                      ignored if no free water estimation.
                      Defaults: 1 tensor-0.0025; 2 tensor-0.0015.
                      Suggested Range: 0.00001-0.25.
                      Default of 0.0 indicates the program will assign value
                      based on other model parameters. (default: 0))""")
    ql = traits.Float(argstr='--Ql %f',
                      desc="""UKF data fitting parameter for tensor model:
                      Process noise for eigenvalues.
                      Defaults: 1 tensor-300 ; 2 tensor-50 ; 3 tensor-100.
                      Suggested Range: 1-1000.
                      Default of 0.0 indicates the program will assign value
                      based on other model parameters.""")
    recordTensors = traits.Bool(argstr='--recordTensors',
                                desc="""Record output from tensor model:
                                Save the tensors that were computed
                                during tractography (if using tensor model).
                                The fields will be called 'TensorN', where N
                                is the tensor number.
                                Recording the tensors enables Slicer to color
                                the fiber bundles by FA, orientation, etc.
                                Recording the tensors also enables quantitative
                                analyses.""")
    recordFreeWater = traits.Bool(argstr='--recordFreeWater',
                                  desc="""Record output from tensor
                                  plus free water model:
                                  Save the fraction of free water.
                                  Attaches field 'FreeWater' to fiber.""")
    recordTrace = traits.Bool(argstr='--recordTrace',
                              desc="""Record output from tensor model:
                              Save the trace of the tensor(s).
                              Attaches field 'Trace' or 'Trace1' and 'Trace2'
                              for 2-tensor case to fiber.""")
    recordFA = traits.Bool(argstr='--recordFA',
                           desc="""Record output from tensor model:
                           Save fractional anisotropy (FA) of the tensor(s).
                           Attaches field 'FA' or 'FA1' and 'FA2' for 2-tensor
                           case to fiber.""")
    freeWater = traits.Bool(argstr='--freeWater',
                            desc="""Adds a term for free water diffusion
                            to the model. The free water model is a tensor
                            with all 3 eigenvalues equal to the diffusivity of
                            free water (0.003).
                            To output the free water fraction, make sure to
                            use the 'save free water' parameter.""")
    recordNMSE = traits.Bool(argstr='--recordNMSE',
                             desc="""Record output from data fitting:
                             Store normalized mean square error
                             (NMSE) along fibers.""")
    maxHalfFiberLength = traits.Float(argstr='--maxHalfFiberLength %f',
                                      desc="""Tractography parameter used in
                                      all models.
                                      The max length limit of the half fibers
                                      generated during tractography.
                                      A fiber is 'half' when the tractography
                                      goes in only one direction from one seed
                                      point at a time.
                                      Default: 250 mm. Range: 1-500 mm.""")
    recordLength = traits.Float(argstr='--recordLength %f',
                                desc="""Tractography parameter used in
                                all models. Step size between points saved
                                along fibers.
                                Default: 0.9. Range: 0.1-4.""")
    qm = traits.Float(argstr='--Qm %f',
                      desc="""UKF data fitting parameter for tensor or NODDI
                      model:
                      Process noise for angles/direction.
                      Defaults: Noddi-0.001; Single tensor-0.005; other-0.001.
                      Suggested Range: 0.00001 - 0.25.
                      Default of 0.0 indicates the program will assign value
                      based on other model parameters.""")
    stepLength = traits.Float(argstr="--stepLength %f",
                              desc="""Tractography parameter used in all
                              models.
                              Step size when conducting tractography.
                              Default: 0.3. Range: 0.1-1. (default: 0.3)""")
    numTensor = traits.Enum(1, 2,
                            argstr="--numTensor %d",
                            desc="""Number of tensors (tensor model)
                            or orientations (NODDI model) used.
                            Default: 2; max: 2""")
    numThreads = traits.Int(argstr="--numThreads %d",
                            desc="""Tractography parameter used in all models.
                            Number of threads used during computation.
                            Set to the number of cores on your workstation for
                            optimal speed. If left undefined, the number of
                            cores detected will be used.
                            Default: -1""")
    minGA = traits.Float(argstr='--minGA %f',
                         desc="""Tractography parameter used in all models.
                         Tractography will stop when the generalized anisotropy
                         (GA) is less than this value. GA is a normalized
                         variance of the input signals (so it does not depend
                         on any model).
                         Note: to extend tracking through low anisotropy areas,
                         this parameter is often more effective than the minFA.
                         This parameter is used by both tensor and NODDI
                         models.
                         Default: 0.1. Range: 0-1.""")
    minFA = traits.Float(argstr='--minFA %f',
                         desc="""Tractography parameter used in tensor model.
                         Tractography will stop when the fractional anisotropy
                          (FA) of the tensor being tracked is less than this
                          value.
                          Note: make sure to also decrease the GA to track
                          through lower anisotropy areas.
                          This parameter is used only in tensor models.
                          Default: 0.15. Range: 0-1.""")
    seedFALimit = traits.Float(argstr='--seedFALimit %f',
                               desc="""Tractography parameter used in all
                               models. Seed points whose fractional anisotropy
                                (FA) are below this value are excluded.
                               Default: 0.18. Range: 0-1.""")
    seedsPerVoxel = traits.Int(argstr='--seedsPerVoxel %d',
                               desc="""Tractography parameter used in all
                                models.
                               Each seed generates a fiber, thus using more
                                seeds generates more fibers. In general use
                                1 or 2  seeds, and for a more thorough result
                                use 5 or 10 (depending on your machine this may
                                take up to 2 days to run).
                               Default: 1. Range: 0-50.""")
    tracts = SingularityFile(argstr='--tracts %s',
                             desc="""Output fiber tracts.""",
                             name_source=['dwiFile'],
                             name_template='%s_tracts.vtk',
                             hash_files=False)
    maskFile = SingularityFile(argstr='--maskFile %s',
                               desc=("Brain mask for diffusion tractography."
                                     " Tracking will only be performed inside"
                                     " this mask"))
    labels = SingularityFile(argstr='--labels %s',
                             desc=("A vector of the ROI labels to be used."
                                   "These are the voxel values where "
                                   "tractography should be seeded. "
                                   "Default: 1"))
    seedsFile = SingularityFile(argstr='--seedsFile %s',
                                desc=("Seeds for diffusion."
                                      "If not specified, full brain "
                                      "tractography will be performed, and "
                                      "the algorithm will start from every "
                                      "voxel in the brain mask where the "
                                      "Generalized Anisotropy is bigger "
                                      "than 0.18."))
    dwiFile = SingularityFile(argstr='--dwiFile %s',
                              desc="""Input diffusion weighted (DWI) file.""",
                              exists=True)
    version = traits.Bool(argstr='--version',
                          desc="""Displays version and exits""")


class UKFTractographyOutputSpec(TraitedSpec):
    tracts = SingularityFile(desc="Output fiber tracts", exists=True)
    returnParameterFile = File(desc="Output parameter file", exists=False)


class UKFTractographyTask(SingularityTask):
    input_spec = UKFTractographyInputSpec
    output_spec = UKFTractographyOutputSpec
    container_cmd = None

    def __init__(self, **inputs):
        super(UKFTractographyTask, self).__init__(**inputs)

    def _list_outputs(self):
        super(UKFTractographyTask, self)._list_outputs()
        outputs = self.output_spec().get()
        outputs['returnParameterFile'] = self.inputs.returnParameterFile
        outputs['tracts'] = self.inputs.tracts
        import pdb; pdb.set_trace()
        return outputs
