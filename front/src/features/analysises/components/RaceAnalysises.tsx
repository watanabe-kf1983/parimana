import { Typography } from '@mui/material';
import { RaceAnalysisesProps } from '../types';
import { Analysis } from './Analysis';


export function RaceAnalysises(props: RaceAnalysisesProps) {

  //   const [status, setStatus] = useState<Status>({ "is_processing": false, "has_result": false })

  //   useEffect(() => {
  //     const getStatus = async () => {
  //       const response = await axios.get(`http://127.0.0.1:5000/analyse/status/${props.raceId}`);
  //       setStatus(response.data)
  //     }
  //     getStatus()
  //   }, [props.raceId])


  return (
    <>
      <Typography variant="h2">
        RaceAnalysis
      </Typography>
      <Typography variant="body1">
        for {props.raceId}
      </Typography>
      <Analysis raceId={props.raceId} modelName="no_cor" />
      <Analysis raceId={props.raceId} modelName="ppf_mtx" />
    </>
  )
}
