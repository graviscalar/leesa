import os
import fnmatch
import zipfile
import shutil
import subprocess


# ----------------------------------------------------------------------------------------------------------------------
# --- Create directory or delete all files there
#
# directory:            directory name
# pattern:              pattern to search for erase
#
# return:       none
# ----------------------------------------------------------------------------------------------------------------------
def dir_create_erase(directory: str, pattern: list) -> None:
    """
    Create directory or delete all files there

    :param directory: directory name
    :param pattern: pattern to search for erase. example - ['*.png', '*.jpg', '*.json']
    :return: None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("The directory {0} created".format(directory))
    else:
        dir_delete_all_files(directory, pattern)


def dir_delete_all_files(directory: str, pattern: list) -> int:
    """
   Delete all files in particular directory

    :param directory: search all files within directory
    :param pattern: pattern to search for erase. example - ['*.png', '*.jpg', '*.json']
    :return: the number of deleted files
    """
    print("Erasing files in directory ", directory, " procedure started")
    i = 0
    for root, dirs, files in os.walk(directory):
        for basename in files:
            for e in pattern:
                if fnmatch.fnmatch(basename, e):
                    file_name = os.path.join(root, basename)
                    os.remove(file_name)
                    i += 1
    print("Erased {0} files".format(i))
    print("Erasing files in directory ", directory, " procedure complete")
    return i


def dir_get_all_files(directory: str):
    """
    Return list of all files in particular directory

    :param directory: search all files within directory
    :return: the list of files
    """
    files_list = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            files_list.append(filepath)
    return files_list


# # ----------------------------------------------------------------------------------------------------------------------
# # --- Return list of the all files in particular directory
# #
# # directory:            search all files within directory:
# # pattern:              pattern to search
# #
# # return:       list of files, quantity of files
# # ----------------------------------------------------------------------------------------------------------------------
# def ts_directory_get_list_off_all_files(directory: str, pattern: list) -> tuple:
#     file_list = []
#     print("Gathering files in directory ", directory, " procedure started")
#     for root, dirs, files in os.walk(directory):
#         for basename in files:
#             for e in pattern:
#                 if fnmatch.fnmatch(basename, e):
#                     file_name = os.path.join(root, basename)
#                     file_list.append(file_name)
#     print("Gathered {0} files".format(len(file_list)))
#     print("Gathering files in directory ", directory, " procedure complete")
#     return file_list, len(file_list)
#
#
# # ----------------------------------------------------------------------------------------------------------------------
# # --- Return list of pairs as image and json
# #
# # ----------------------------------------------------------------------------------------------------------------------
# def ts_get_image_json_pair(directory_img: str, pattern_img: list, directory_json: str, pattern_json: list) -> tuple:
#     result = True
#     pairs = []
#     fl_img, qy_img = ts_directory_get_list_off_all_files(directory_img, pattern_img)
#     fl_json, qy_json = ts_directory_get_list_off_all_files(directory_json, pattern_json)
#     if qy_img == qy_json:
#         # search by image list
#         for e in fl_img:
#             img_ne = os.path.splitext(os.path.basename(e))
#             search = False
#             for s in fl_json:
#                 json_ne = os.path.splitext(os.path.basename(s))
#                 if img_ne[0] == json_ne[0]:
#                     pairs.append([e, s])
#                     search = True
#                     break
#             if search is False:
#                 print("The image file {0} is not paired with JSON file".format(e))
#                 result = False
#                 break
#         if result is True:
#             print("The {0} pairs of image and JSON is gathered".format(len(pairs)))
#     else:
#         result = False
#         print("Incorrect number of pairs. Gathered {0} images and {1} JSON files".format(qy_img, qy_json))
#
#     return result, pairs
#
#
# def ts_directory_zip_and_delete_all_files(directory: str, v_zip_fn: str, pattern: list) -> int:
#     print("Compressing and Erasing files in directory ", directory, " procedure started")
#     i = 0
#     zip_fn = directory + '/' + v_zip_fn
#     zip_f = zipfile.ZipFile(zip_fn, 'w', zipfile.ZIP_DEFLATED)
#     for root, dirs, files in os.walk(directory):
#         for basename in files:
#             for e in pattern:
#                 if fnmatch.fnmatch(basename, e):
#                     file_name = os.path.join(root, basename)
#                     zip_f.write(file_name)
#                     os.remove(file_name)
#                     i += 1
#     print("Compressed and Erased {0} files".format(i))
#     print("Compressing and Erasing files in directory ", directory, " procedure complete")
#     return i
#
#
# def ts_copytree(src, dst, symlinks=False, ignore=None):
#     for item in os.listdir(src):
#         s = os.path.join(src, item)
#         d = os.path.join(dst, item)
#         if os.path.isdir(s):
#             shutil.copytree(s, d, symlinks, ignore)
#         else:
#             shutil.copy2(s, d)
#
#
# def ffmpeg_video_from_images(p_dir_img: str = None,
#                              p_img_zfill: int = 5,
#                              p_img_ext: str = 'png',
#                              p_video_out: str = None,
#                              p_fps_input: int = 30,
#                              p_fps_output: int = 30,
#                              p_codec: str = 'libx264',
#                              p_profile: str = 'high'):
#     if p_codec == 'libx265':
#         p_profile = 'main'
#     img_seq = p_dir_img + '/' + '%0{0}d.{1}'.format(p_img_zfill, p_img_ext)
#     str_ffmpeg = 'ffmpeg -r {fps_input} ' \
#                  '-i {video} ' \
#                  '-c:v {codec} ' \
#                  '-preset slow ' \
#                  '-profile:v {profile} ' \
#                  '-crf 18 -coder 1 -pix_fmt yuv420p ' \
#                  '-movflags +faststart -g 30 -bf 2 -c:a aac -b:a 384k -profile:a aac_low ' \
#                  '-r {fps_output} ' \
#                  '{output}'.format(fps_input=p_fps_input,
#                                    video=img_seq,
#                                    codec=p_codec,
#                                    profile=p_profile,
#                                    fps_output=p_fps_output,
#                                    output=p_video_out)
#     subprocess.call(str_ffmpeg, shell=True)
