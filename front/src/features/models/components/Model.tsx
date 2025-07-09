import { Competence, CorrelationData } from '../types';
import { Competences } from './Competences';
import { Correlation } from './Correlation';

type Props = {
  modelName: string,
  competences: Array<Competence>,
  correlations: Array<CorrelationData>,
  competencesChart: string,
  correlationsChart: string,
}

export function Model(props: Props) {
  switch (props.modelName) {
    case 'ppf_mtx':
      return <CorModel {...props} />;
    case 'no_cor':
      return <NoCorModel {...props} />;
    default:
      return null;
  }
}

function CorModel(props: Props) {
  return (
    <>
      <Competences competences={props.competences} chart={props.competencesChart} />
      <Correlation correlations={props.correlations} chart={props.correlationsChart} />
    </>
  );
}

function NoCorModel(props: Props) {
  return (
    <>
      <Competences competences={props.competences} chart={props.competencesChart} />
    </>
  );
}
