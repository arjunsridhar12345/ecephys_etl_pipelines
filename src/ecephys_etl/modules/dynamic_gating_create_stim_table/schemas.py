from argschema import ArgSchema
from argschema.fields import (LogLevel, InputFile, Nested, OutputFile, Float)

from ecephys_etl.schemas.fields import OutputFileExists


class DynamicGatingCreateStimulusTableInputSchema(ArgSchema):
    log_level = LogLevel(
        default="INFO",
        description="The logging level for the module."
    )
    sync_h5_path = InputFile(
        required=True,
        description=(
            "Path to an hdf5 file (with *.sync extension) that contains "
            "timing synchronization information to align stimulus "
            "presentation and behavior timestamps with ecephys data "
            "timestamps."
        )
    )
    behavior_pkl_path = InputFile(
        required=True,
        description=(
            "Path to a python *.pkl file that contains information about "
            "stimulus presentations, rewards, trials, and running speed "
            "during an active portion of an ecephys session."
        )
    )
    mapping_pkl_path = InputFile(
        required=True,
        description=(
            "Path to a python *.pkl file that contains information about "
            "stimulus presentations for a passive portion of an ecephys "
            "session. Information about stimuli presented are used for "
            "receptive field mapping."
        )
    )
   
    replay_pkl_path = InputFile(
        required=False,
        description=(
            "Path to a python *.pkl file that contains information about "
            "an exact playback of stimuli during the behavior portion of a "
            "session (specified in behavior_pkl_path) except without "
            "rewards."
        )
    )
    frame_time_offset = Float(
        required=False,
        default=0.008,
        allow_none=False,
        description=(
            "Scalar value (in seconds) to be added to the "
            "start_time and stop_time columns based on empirical "
            "hardware measurements (default value is taken from "
            "experiments done leading up to the VBN 2022 data "
            "release)"))
    output_stimulus_table_path = OutputFile(
        required=True,
        description=(
            "Path where *.csv stimulus table output should be written to."
        )
    )


class VbnCreateStimulusTableOutputSchema(ArgSchema):
    input_parameters = Nested(
        DynamicGatingCreateStimulusTableInputSchema,
        required=True,
        description=(
            "Input parameters that the vbn_create_stimulus_table module "
            "was run with."
        )
    )
    output_path = OutputFileExists(
        required=True,
        description=(
            "The output stimulus_table *.csv file synthesized from the "
            "input *.pkl files + *.sync file."
        )
    )
