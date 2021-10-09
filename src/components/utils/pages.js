export const getPageCount = (totalCount, limit) => {
    return Math.ceil(totalCount/limit)
}

export const getPagesArray = (curPage, totalPages) => {
    let result = []
    let start = Math.floor(curPage / 10) * 10
    let start_index = start === 0 ? start + 1 : start;
    let end = start_index + 10 > totalPages ? totalPages : start_index + 10;
    let end_index = start_index === 1 ? end - 1 : end;

    console.log(start_index, end_index, totalPages)

    for (let i=start_index; i<=end_index; i++) {
        result.push(i)
    }
    return result;
}