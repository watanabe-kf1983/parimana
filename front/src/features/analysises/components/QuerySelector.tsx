import { useState } from 'react'
import { TextField } from '@mui/material';
import { QuerySelectorProps } from '../types';
import { FilterAlt } from '@mui/icons-material';

export function QuerySelector(props: QuerySelectorProps) {
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

