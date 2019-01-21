import pandas as pd
import xml.etree.ElementTree as ET


def explore_dict(number, dict, files):
    """Short summary.
    Function returns pandas dataframe from dictionary with the name of a raport
    Parameters
    ----------
    number : type
        Number of dictionary to explore. Starts from 0.
    dict : type
        Dictionary with pandas dataframes.
    files : type
        Files to get.

    Returns
    -------
    type
        Description of returned object.

    """
    f = files[number]
    print('Raport name is -' + f)
    d = dict[f]
    return(d)


def xml_to_dict(root):
    """Short summary.
    Functions converts xml object from AWS api into more usefull dictionary object.
    Function is still in development

    Parameters
    xml root file generated by xml.etree.ElementTree module
    Example:
    tree = xml.etree.ElementTree.parse(xml)
    root = tree.getroot()

    root : type
        Description of parameter `root`.


    Returns
    dictionary object
    type
        {}

    """

    all_files = root.getchildren()[0].getchildren()
    first_order = []
    for find_timeFrame in all_files:
        has_time_frame = find_timeFrame.find('timeFrame')
        if has_time_frame is not None:
            first_order.append(find_timeFrame.tag)

    d = {}
    for files in all_files:
        if files.tag in first_order:
            tf = files.find('timeFrame')
            s_ = pd.to_datetime(tf.find('start').text[:10])
            e_ = pd.to_datetime(tf.find('end').text[:10])
            diff_ = (e_ - s_).days + 1
            value = files.find('defectCount').text
            tag_ = str(files.tag) + "_" + str(diff_)
            if tag_ in d.keys():
                if value is not None:
                    d[tag_].append(value)
                else:
                    d[tag_].append('')
            else:
                if value is not None:
                    d[tag_] = value
                else:
                    d[tag_] = ''
        elif files.tag == 'performanceChecklist':
            for metric in files:
                status = metric.find('status').text
                tag_ = str(metric.tag) + '_status'
                if tag_ in d.keys():
                    if status is not None:
                        d[tag_].append(status)
                    else:
                        d[tag_].append('')
                else:
                    if status is not None:
                        d[tag_] = status
                    else:
                        d[tag_] = ''
        else:
            for file in files:
                tf = file.find('timeFrame')
                s_ = pd.to_datetime(tf.find('start').text[:10])
                e_ = pd.to_datetime(tf.find('end').text[:10])
                diff_ = (e_ - s_).days + 1
                for element in file:
                    if element.tag != 'timeFrame':
                        if len(element):
                            rate_ = element.find('rate').text
                            tag_ = str(element.tag) + '_' + str(diff_) + '_rate'
                        else:
                            rate_ = element.text
                            tag_ = str(element.tag) + '_' + str(diff_)
                        if tag_ in d.keys():
                            if rate_ is not None:
                                d[tag_].append(rate_)
                            else:
                                d[tag_].append('')
                        else:
                            if rate_ is not None:
                                d[tag_] = rate_
                            else:
                                d[tag_] = ''

    return(d)
