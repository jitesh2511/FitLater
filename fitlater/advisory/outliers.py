from fitlater.advisory.util import build_advice

def handle_outliers(column, data, profile):

    outlier_percentage = data['outlier_percentage']
    if outlier_percentage > 30:
        recommendation = 'Investigate data or consider dropping column'
        reason = f'High percentage of outliers may indicate data issues. Outlier percentage is {outlier_percentage}%'
        priority = 1

    elif outlier_percentage:
        recommendation = 'Apply capping'
        reason = f'Moderate outliers can distort model performance. Outlier percentage is {outlier_percentage}%'
        priority = 2
        
    else:
        recommendation = 'Consider removing outliers'
        reason = f'Small number of outliers have limited impact. Outlier percentage is {outlier_percentage}%'
        priority = 3
        
    return build_advice(column, 'outliers', recommendation, reason, priority)