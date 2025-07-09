import { useState, Dispatch, SetStateAction } from 'react'
import { TextField } from '@mui/material';
import { FilterAlt } from '@mui/icons-material';

type Props = { query: string, onSetQuery: Dispatch<SetStateAction<string>> };

export function QuerySelector(props: Props) {
    const [query, setQuery] = useState<string>(props.query)

    const onQueryEntered = () => {
        props.onSetQuery(query);
    }

    return (
        <>
            <FilterAlt />
            <TextField
                // sx={{ display: 'none' }}
                size='small'
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                        onQueryEntered();
                    }
                }}
                onBlur={onQueryEntered} />
        </>
    )
}

