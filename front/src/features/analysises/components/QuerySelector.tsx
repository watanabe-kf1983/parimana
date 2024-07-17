import { useState } from 'react'
import { TextField } from '@mui/material';
import { QuerySelectorProps } from '../types';

export function QuerySelector(props: QuerySelectorProps) {
    const [query, setQuery] = useState<string>(props.query)

    const onQueryEntered = () => {
        props.onSetQuery(query);
    }

    return (
        <TextField
            sx={{ m: 1, width: '350px' }}
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={(e) => {
                if (e.key === 'Enter') {
                    onQueryEntered();
                }
            }}
            onBlur={onQueryEntered} />
    )
}

