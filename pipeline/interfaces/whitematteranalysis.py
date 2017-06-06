"""
Nipype interface for whitemattertractography suite
"""

from .singularity import (SingularityInputSpec,
                          SingularityTask,
                          SingularityFile,
                          SingularityDir)

from nipype.interfaces.base import (traits,
                                    TraitedSpec,
                                    File,
                                    Directory)

from nipype.external.due import BibTeX

import os


class WmRegisterToAtlasNewInputSpec(SingularityInputSpec):
    inputSubject = SingularityFile(argstr="%s",
                                   position=1,
                                   desc=("One subject data: "
                                         "whole-brain tractography as vtkPoly data "
                                         "(.vtk or .vtp)"),
                                   exists=True)
    inputAtlas = SingularityFile(argstr="%s",
                                 position=2,
                                 desc=("An atlas, one file containing whole-brain "
                                       "tractography as vtkPolyData (.vtk or .vtp)"))

    outputDirectory = SingularityDir(argstr="%s",
                                     position=3,
                                     desc="Will be created if it doesn't exist",
                                     name_source=['inputSubject'],
                                     name_template='%s_RegisterToAtlas/')

    mode = traits.Enum('affine', 'nonrigid',
                       argstr="-mode %s")

    numberOfFibers = traits.Int(desc=("Total number of fibers to analyse "
                                      "from each dataset. During registration "
                                      "at each iteration fibers are randomly "
                                      "sampled from within this data."
                                      "20000 us the default number of total"
                                      "fibers."),
                                argstr="-f %d")
    fiberLength = traits.Int(desc=("Minimum length (in mm) of fibers to "
                                   "analyze. Default:20mm."),
                             argstr="-l %d")
    fiberLengthMax = traits.Int(desc=("Maximum length (in mm) of fibers to "
                                      "analyse. This parameter can be used to "
                                      "remove extremely long fibers that may "
                                      "have traversed several structures."
                                      "For example, a value of 200 will "
                                      "avoid sampling the tail end of the "
                                      "fiber length distribution."
                                      "Default: 260mm"),
                                argstr="-lmax %d")
    verbose = traits.Bool(desc=("Verbose. Store more files and images of "
                                "ontermediate and final polydatas."),
                          argstr="-verbose")


class WmRegisterToAtlasNewOutputSpec(TraitedSpec):
    """Output spec"""
    outputFile = SingularityFile(desc="Registered tracts")
    outputDirectory = SingularityDir(desc="Output directory")


class WmRegisterToAtlasNewTask(SingularityTask):
    container_cmd = 'wm_register_to_atlas_new.py'
    input_spec = WmRegisterToAtlasNewInputSpec
    output_spec = WmRegisterToAtlasNewOutputSpec

    references_ = [{'entry': BibTeX("@article{ODonnell2012,"
                                    "author = {O'Donnell, Lauren J and Wells, William M and Golby, Alexandra J and Westin, Carl-Fredrik},"
                                    "journal = {Medical image computing and computer-assisted intervention : MICCAI ... International Conference on Medical Image Computing and Computer-Assisted Intervention},"
                                    "number = {Pt 3},"
                                    "pages = {123--30},"
                                    "pmid = {23286122},"
                                    "title = {{Unbiased groupwise registration of white matter tractography.}},"
                                    "url = {http://www.ncbi.nlm.nih.gov/pubmed/23286122 http://www.pubmedcentral.nih.gov/articlerender.fcgi?artid=PMC3638882},"
                                    "volume = {15},"
                                    "year = {2012}"
                                    "}")}]

    def _list_outputs(self):
        outputs = self.output_spec().get()
        input_file, _ = os.path.splitext(
            os.path.basename(self.inputs.inputSubject))
        outfile = os.path.join(self.inputs.outputDirectory,
                               input_file,
                               'output_tractography',
                               input_file + '_reg.vtk')
        outputs['outputFile'] = os.path.abspath(outfile)
        outputs['outputDirectory'] = self.inputs.outputDirectory
        return(outputs)


class WmClusterFromAtlasInputSpec(SingularityInputSpec):
    """Input spec for wm_cluster_from_atlas.py"""
    inputFile = SingularityFile(desc=("A file of whole-brain tractography."
                                      "vtkPolyData (.vtk or .vtp)"),
                                exists=True,
                                argstr="%s",
                                position=1)

    atlasDirectory = Directory(desc=("The directory containing the atlas."
                                     "Must contain atlas.p and atlas.vtp"),
                               exists=False,
                               argstr="%s",
                               position=2)
    outputDirectory = SingularityDir(desc="Will be created if it does not exist",
                                     argstr='%s',
                                     position=3,
                                     name_source=['inputFile'],
                                     name_template='%s_ClusterFromAtlas/')
    numberOfFibers = traits.Int(desc=("Number of fibers to analyse "
                                      "from each subject."
                                      "Default: all fibers"),
                                argstr="-f %d")
    fiberLength = traits.Int(desc=("Minimum length (in mm) of fibers to "
                                   "analyze. Default:60mm."),
                             argstr="-l %d")
    jobNumber = traits.Int(desc="Number of processors to use.",
                           argstr="-j %d")
    verbose = traits.Bool(desc=("Verbose. Store more files and images of "
                                "ontermediate and final polydatas."),
                          argstr="-verbose")
    mrmlFibers = traits.Int(desc=("Approximate upper limit on number of fibers "
                                  "to show when MRML scene of clusters is "
                                  "loaded into slicer.Default is 10000 fibers; "
                                  "increase for computers with more memory. "
                                  "Note this can be edited later in the MRML "
                                  "file by searching for SubsamplingRatio and "
                                  "editing that number throughout the file. "
                                  "Be sure to use a text editor program "
                                  "(save as plain text format). "
                                  "An extra MRML file will be saved for "
                                  "visualizing 100% of fibers."),
                            argstr="-mrml_fibers %d")
    registerToSubject = traits.Bool(desc=("To cluster in individual subject "
                                          "space, register atlas polydata to "
                                          "subject. Otherwise, by default this "
                                          "code assumes the subject has "
                                          "already been registered to the "
                                          "atlas."),
                                    argstr="-reg")
    noRender = traits.Bool(desc=("No Render. Prevents rendering of images "
                                 "that would require an X connection. "
                                 "Default: True"),
                           argstr="-norender",
                           value=True)


class WmClusterFromAtlasOutputSpec(TraitedSpec):
    """Input spec for wm_cluster_from_atlas.py"""
    outputDirectory = SingularityDir(desc="Clustered tracts.")


class WmClusterFromAtlasTask(SingularityTask):
    """Use wm_cluster_from_atlas.py to cluster subject fibers"""
    container_cmd = 'wm_cluster_from_atlas.py'
    input_spec = WmClusterFromAtlasInputSpec
    output_spec = WmClusterFromAtlasOutputSpec

    references_ = [{'entry': BibTeX("@article{ODonnell2007,"
                                    "author = {O'Donnell, Lauren J and Westin, Carl-Fredrik},"
                                    "doi = {10.1109/TMI.2007.906785},"
                                    "issn = {0278-0062},"
                                    "journal = {IEEE transactions on medical imaging},"
                                    "month = {nov},"
                                    "number = {11},"
                                    "pages = {1562--75},"
                                    "pmid = {18041271},"
                                    "title = {{Automatic tractography segmentation using a high-dimensional white matter atlas.}},"
                                    "url = {http://www.ncbi.nlm.nih.gov/pubmed/18041271},"
                                    "volume = {26},"
                                    "year = {2007}",
                                    "}")}]

    def _list_outputs(self):
        outputs = self.output_spec().get()
        input_file, _ = os.path.splitext(
            os.path.basename(self.inputs.inputSubject))
        outfile = os.path.join(self.inputs.outputDirectory,
                               input_file + '_reg')
        outputs['outputDirectory'] = os.path.abspath(outfile)
        return(outputs)


class WmClusterRemoveOutliersInputSpec(SingularityInputSpec):
    """Input for wm_cluster_remove_outliers.py"""
    inputDirectory = SingularityDir(desc=("A directory containing subject clusters"
                                     "(.vtp)"),
                               exists=True,
                               position=1,
                               argstr='%s')
    atlasDirectory = SingularityDir(desc=("The directory where the atlas is stored."
                               "Must contain atlas.p and atlas.vtp, "
                               "as well as atlas clusters (.vtp))"),
                               exists=False,
                               position=2,
                               argstr='%s')
    outputDirectory = SingularityDir(desc=("The output directory will be created "
                                      "if it does not exist. "
                                      "Outlier-removed subject clusters will "
                                      "be stored in a subdirectory of the "
                                      "Output directory. The subdirectory "
                                      "will have the same subject id as "
                                      "contained in the input directory."),
                                exists=False,
                                position=3,
                                argstr='%s',
                                name_source=['inputDirectory'],
                                name_template='%s_ClusterFromAtlas/')
    verbose = traits.Bool(desc=("Verbose. Store more files and images of "
                                "ontermediate and final polydatas."),
                          argstr="-verbose")
    clusterOutlierStd = traits.Float(desc=("Reject fiber outliers whose fiber "
                                           "probability (within their cluster) "
                                           "is more than this number of "
                                           "standard deviations below the mean. "
                                           "For more strict rejection, enter a "
                                           "smaller number such as 1.75."
                                           "This probability is measured in an "
                                           "accurate way using pairwise "
                                           "comparison of all fibers in each "
                                           "cluster, to all fibers in the "
                                           "atlas. The purpose of this is to "
                                           "remove outlier fibers accurately "
                                           "within each cluster."
                                           "This parameter can be tuned by the "
                                           "user depending on the amount of "
                                           "outlier fibers present in the "
                                           "tractography, and depending on "
                                           "how strictly outliers were removed "
                                           "in the atlas creation (which "
                                           "will affect estimation of the "
                                           "standard deviation of fiber "
                                           "probabilities in the atlas)."),
                                     argstr="-cluster_outlier_std %f")
    outlierSigma = traits.Float(desc=("(Advanced parameter that probably "
                                      "should not be changed.) "
                                      "Local sigma used to compute fiber "
                                      "probability in cluster-based outlier "
                                      "removal. The default is 20mm."
                                      "For stricter clustering, this may be "
                                      "reduced to 15mm."),
                                argstr="-advanced_only_outlier_sigma %f")


class WmClusterRemoveOutliersOutputSpec(TraitedSpec):
    """Outputs for wm_cluster_remove_outliers.py"""
    outputDirectory = SingularityDir(desc="Clustered tracts.")

class WmClusterRemoveOutliersTask(SingularityTask):
    """Removes outliers in a subject dataset that was
    clustered from a cluster atlas.
    This script uses the atlas to identifies and remove outliers in
    each cluster of the subject. The atlas must be the same one used
    to cluster the subject dataset"""

    container_cmd = 'wm_cluster_remove_outliers.py'
    input_spec = WmClusterRemoveOutliersInputSpec
    output_spec = WmClusterRemoveOutliersOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outfile = os.path.join(self.inputs.outputDirectory,
                               '_outlier_removed')
        outputs['outputDirectory'] = os.path.abspath(outfile)
        return(outputs)

class WmClusterByHemisphereInputSpec(SingularityInputSpec):
    """Inputs for wm_separate_clusters_by_hemisphere.py"""
    inputDirectory = SingularityDir(desc=("A directory of clustered"
                                    "whole-brain tractography as vtkPolyData"
                                    "(.vpk or .vtp)."),
                                    exists=True,
                                    position=1)
    outputDirectory = SingularityDir(desc=("The output directory will be "
                                           "created if it doesnt exist."),
                                     postion=2,
                                     name_source=['inputDirectory'],
                                     name_template='%s_ClusterByHemi/')
    version = traits.Bool(desc="Show programs version and exit",
                          argstr='-v')
    pthresh = traits.Float(desc=("The percent of a fiber that has to be in "
                                 "one hemisphere to consider the fiber as "
                                 "part of that hemisphere (rather than as "
                                 "a commissural fiber). Default number is "
                                 "0.6, where a higher number will tend to "
                                 "label fewer fibers as hemispheric and more "
                                 "fibers as commissural (not strictly in one "
                                 "hemisphere or the other), while a lower "
                                 "number will be stricter about what is "
                                 "classified as commissural."),
                           argstr="-pthresh %d")
    atlasMRML = File(desc=("A MRML file defining the atlas clusters, "
                           "to be copied into all directories."),
                     argstr="-atlasMRML %s")


class WmClusterByHemisphereOutputSpec(TraitedSpec):
    commissural_tracts = Directory(desc=("Directory containing commissural "
                                         "tracts."),
                                   exists=True)
    left_hemi_tracts = Directory(desc=("Directory containing left hemiphere "
                                       "tracts."),
                                 exists=True)
    right_hemi_tracts = Directory(desc=("Directory containing right hemisphere "
                                        "tracts."),
                                  exists=True)


class WmClusterByHemisphereTask(SingularityTask):
    """
    Separate each cluster into left/right/commissural tracts according to the
     percentage of each fiber. The output is three directories of fiber bundles
     according to left hemisphere, right hemisphere, and commissural tracts.
     Also copies any Slicer MRML scene file that is given as input into the
     three separate directories.
    """

    container_cmd = "wm_separate_clusters_by_hemisphere.py"
    input_spec = WmClusterByHemisphereInputSpec
    output_spec = WmClusterByHemisphereOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()

        outfile = os.path.join(self.inputs.outputDirectory,
                               'tracts_commissural')
        outputs['commissural_tracts'] = os.path.abspath(outfile)

        outfile = os.path.join(self.inputs.outputDirectory,
                               'tracts_left_hemisphere')
        outputs['left_hemi_tracts'] = os.path.abspath(outfile)

        outfile = os.path.join(self.inputs.outputDirectory,
                               'tracts_right_hemisphere')
        outputs['right_hemi_tracts'] = os.path.abspath(outfile)

        return(outputs)
