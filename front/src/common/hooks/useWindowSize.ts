import { useLayoutEffect, useState } from 'react';

// https://zenn.dev/kenghaya/articles/6020b6192dadec#hooks%E3%81%AE%E5%AE%9F%E8%A3%85

export const useWindowSize = (): number => {
    const [size, setSize] = useState(400);
    useLayoutEffect(() => {
        const updateSize = (): void => {
            setSize(window.innerWidth);
        };

        window.addEventListener('resize', updateSize);
        updateSize();

        return () => window.removeEventListener('resize', updateSize);
    }, []);
    return size;
};