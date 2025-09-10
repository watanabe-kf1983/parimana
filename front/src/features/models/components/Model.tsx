import { ModelData } from '../types';
import { Competences } from './Competences';
import { Correlation } from './Correlation';

type Props = {
  model: ModelData
}

export function Model(props: Props) {
  switch (props.model.type) {
    case 'ppf_mtx':
      return <CorModel {...props} />;
    case 'yurayura':
      return <NoCorModel {...props} />;
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
