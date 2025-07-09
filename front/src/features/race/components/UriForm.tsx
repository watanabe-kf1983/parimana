import { useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import * as api from "../api";

type Props = {
  onRaceIdFound: (raceId: string) => void;
};

export function UriForm(props: Props) {
  const [open, setOpen] = useState<boolean>(false);
  const [processing, setProcessing] = useState<boolean>(false);
  const [inputValue, setInputValue] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setInputValue('');
    setOpen(false);
  };

  const handleOk = async () => {
    const uri = inputValue
    setProcessing(true);
    try {
      const raceId = await api.findRaceIdByUri(uri);
      if (open) {
        setInputValue('');
        setOpen(false);
        props.onRaceIdFound(raceId)
      }
    } catch (e) {
      setErrorMessage('指定されたURLは利用できません')
    } finally {
      setProcessing(false);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setErrorMessage('')
    setInputValue(event.target.value);
  };

  return (
    <>
      <Button onClick={handleClickOpen} size="small" sx={{ m: 1 }}>
        URL
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        maxWidth="xl">
        <DialogTitle>URLでレースを指定</DialogTitle>
        <DialogContent>
          <DialogContentText>
            オッズ取得元ページのURLで レースを指定します <br />
            （例 https://www.boatrace.jp/owpc/pc/race/odds3t?rno=12&jcd=12&hd=20241222）
          </DialogContentText>
          <TextField
            autoFocus
            error={Boolean(errorMessage)}
            margin="dense"
            id="url"
            name="url"
            label="URL"
            type="text"
            variant="standard"
            fullWidth
            value={inputValue}
            helperText={errorMessage}
            onChange={handleInputChange}
          />
        </DialogContent>
        <DialogActions>
          <Button disabled={processing} onClick={handleClose}>キャンセル</Button>
          <Button disabled={processing} onClick={handleOk} type="submit">OK</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
