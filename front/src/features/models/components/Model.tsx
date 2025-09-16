import { Typography } from '@mui/material';
import { ModelData } from '../types';
import { Competences } from './Competences';
import { CompetencesMulti } from './CompetencesMulti';
import { Correlation } from './Correlation';

type Props = {
  model: ModelData
}

export function Model(props: Props) {
  if (!props.model) {
    return <Typography variant="body1"> No model data available.</Typography>
  }
  switch (props.model.type) {
    case 'ppf_mtx':
      return <CorModel {...props} />;
    case 'yurayura':
      return <YuraModel {...props} />;
    case 'no_cor':
      return <NoCorModel {...props} />;
    default:
      return null;
  }
}

function CorModel(props: Props) {
  return (
    <>
      <Competences competences={props.model.competences} chart={props.model.competences_chart} />
      <Correlation correlations={props.model.correlations} chart={props.model.correlations_chart} />
    </>
  );
}

function NoCorModel(props: Props) {
  return (
    <>
      <Competences competences={props.model.competences} chart={props.model.competences_chart} />
    </>
  );
}

function YuraModel(props: Props) {
  return (
    <>
      <CompetencesMulti competences_by_places={props.model.competences_by_places} chart={props.model.competences_chart} />
    </>
  );
}
