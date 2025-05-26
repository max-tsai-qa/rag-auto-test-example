

def assert_majority(threshold: float, judges: list[dict]) -> None:
    """
    :param judge:
        The judge param with llm response
    :param threshold:
        The threshold param with eval score, should be float and between 0 and 10
    """
    if not judges:
        raise ValueError('judges must be a list of dictionaries and should not be empty')
    
    if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 10:
        raise ValueError('threshold must be a number between 0 and 10 and should not be empty')
    
    sum_scores = sum(judge.get('score', 0) for judge in judges)
    if sum_scores > len(judges) * threshold:
        return
    
    failed_metrics_str = '\n\n'.join(
        [
            f'judge: {judge.get("model_name", "N/A")}, score: {judge.get("score")}, reason: {judge.get("reason")}'
            for judge in judges
        ]
    )
    
    raise AssertionError(f'assert_majority threshold={threshold} failed: \n{failed_metrics_str}')
