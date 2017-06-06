from ..interfaces import ukftractography as ukf
from ..interfaces import whitematteranalysis as wma

from nipype import SelectFiles, Node, Workflow

wm_container = '/archive/code/containers/WHITEMATTERANALYSIS/whitematteranalysis.img'
ukf_container = '/archive/code/containers/UKFTRACTOGRAPHY/ukftractography.img'
maps = ['/scratch/twright/data/dtiprep:/input']

# Define the pipeline nodes
tract = Node(ukf.UKFTractographyTask(container=ukf_container,
                                     map_dirs_list=maps,
                                     recordFreeWater=True,
                                     freeWater=True,
                                     numTensor=2,
                                     seedsPerVoxel=5),
             name="tractography")

register = Node(wma.WmRegisterToAtlasNewTask(container=wm_container,
                                             map_dirs_list=maps,
                                             inputAtlas='/opt/atlases/atlas.vtp'),
                name="RegisterToAtlas")
cluster = Node(wma.WmClusterFromAtlasTask(container=wm_container,
                                          map_dirs_list=maps,
                                          atlasDirectory='/opt/atlases',
                                          fiberLength=20),
               name="ClusterFromAtlas")
outliers = Node(wma.WmClusterRemoveOutliersTask(container=wm_container,
                                                map_dirs_list=maps,
                                                atlasDirectory='/opt/atlases',
                                                clusterOutlierStd=4),
                name="RemoveOutliers")
splits = Node(wma.WmClusterByHemisphereTask(container=wm_container,
                                            map_dirs_list=maps,
                                            atlasMRML='/opt/atlases/clustered_tracts_display_100_percent_aem.mrml'),
              name="ClusterByHemisphere")

# Define the file selector

templates = {'dwi': 'dtiprep/{subject_id}/{subject_id}_0[1,2]_DTI60-1000_20_Ax-DTI-60plus5_QCed.nrrd',
             'mask': 'dtiprep/{subject_id}/{subject_id}_0[1,2]_DTI60-1000_20_Ax-DTI-60plus5_QCed_B0_threshold_masked.nrrd'}

sf = Node(SelectFiles(templates),
          name="selectFiles")

sf.inputs.subject_id = 'SPN01_CMH_0001_01'
sf.inputs.base_directory = '/scratch/twright/data'

# Connect everything together
wf = Workflow(name="2tensor", base_dir="working_dir")
wf.connect([(sf, tract, [("dwi", "dwiFile"),
                         ("mask", "maskFile")]),
            (tract, register, [("tracts", "inputSubject")]),
            (register, cluster, [("outputFile", "inputFile")]),
            (cluster, outliers, [("outputDirectory", "inputDirectory")]),
            (outliers, splits, [("outputDirectory", "inputDirectory")])])


wf.connect([(sf, tract, [("dwi", "dwiFile"),
                         ("mask", "maskFile")]),
            (tract, register, [("tracts", "inputSubject")])])
