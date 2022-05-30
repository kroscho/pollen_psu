import { useState } from "react";

export const useFetching = (callback:any) => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setErrror] = useState('');

    const fetching = async () => {
        try {
            setIsLoading(true)
            await callback()
        } catch (err) {
            let errMessage = "";
            if (err instanceof Error) {
                errMessage = err.message;
            }
            console.log(errMessage);
            setErrror(errMessage)
        } finally {
            setIsLoading(false);
        }
    }
    return [fetching, isLoading, error] as const
}