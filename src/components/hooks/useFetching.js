import { useState } from "react";

export const useFetching = (callback) => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setErrror] = useState('');

    const fetching = async () => {
        try {
            setIsLoading(true)
            await callback()
        } catch (e) {
            setErrror(e.message);
        } finally {
            setIsLoading(false);
        }
    }
    return [fetching, isLoading, error]
}