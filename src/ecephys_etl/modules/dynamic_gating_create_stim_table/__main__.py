import pandas as pd
import argschema

from ecephys_etl.modules.dynamic_gating_create_stim_table.schemas import (
    DynamicGatingCreateStimulusTableInputSchema,
    VbnCreateStimulusTableOutputSchema
)
from ecephys_etl.data_extractors.sync_dataset import Dataset
from ecephys_etl.data_extractors.stim_file import (
    CamStimOnePickleStimFile,
    BehaviorPickleFile,
    ReplayPickleFile
)
from ecephys_etl.modules.dynamic_gating_create_stim_table.create_dynamic_gating_stim_table import (
    create_dynamic_gating_stimulus_table
)


class DynamicGatingCreateStimulusTable(argschema.ArgSchemaParser):
    default_schema = DynamicGatingCreateStimulusTableInputSchema
    default_output_schema = VbnCreateStimulusTableOutputSchema

    def run(self):
        self.logger.name = type(self).__name__
        output_path = self.args["output_stimulus_table_path"]
        sync_data = Dataset(self.args["sync_h5_path"])

        behavior_pkl_path = self.args["behavior_pkl_path"]
        behavior_data = BehaviorPickleFile.factory(behavior_pkl_path)

        mapping_pkl_path = self.args["mapping_pkl_path"]
        mapping_data = CamStimOnePickleStimFile.factory(mapping_pkl_path)

        #replay_data = ReplayPickleFile.factory(self.args["replay_pkl_path"])

        stim_table: pd.DataFrame = create_dynamic_gating_stimulus_table(
            sync_dataset=sync_data,
            behavior_pkl=behavior_data,
            mapping_pkl=mapping_data,
            frame_time_offset=self.args["frame_time_offset"]
        )
        stim_table.to_csv(path_or_buf=output_path, index=False)

        output_data = {
            "input_parameters": self.args,
            "output_path": output_path
        }

        self.output(output_data, indent=2)


if __name__ == "__main__":  # pragma: nocover
    stim_table_maker = DynamicGatingCreateStimulusTable()
    stim_table_maker.run()
