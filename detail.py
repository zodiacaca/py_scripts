
import os
import pythoncom
import pywintypes
from win32com.propsys import propsys, pscon
from win32com.shell import shell, shellcon

editable_keynames = set([
  'PKEY_Title',
  'PKEY_Comment',
  'PKEY_Music_TrackNumber',
  'PKEY_Music_PartOfSet',
  'PKEY_Author',
  'PKEY_Rating',
  'PKEY_Keywords',
  'PKEY_Music_AlbumArtist',
  'PKEY_Music_AlbumTitle',
  'PKEY_Music_Composer',
  'PKEY_Media_SubTitle',
  'PKEY_Media_PromotionUrl',
  'PKEY_Video_Director',
  'PKEY_Subject',
  'PKEY_Media_AuthorUrl',
  'PKEY_Music_TrackNumber',
  'PKEY_Media_EncodingSettings',
  'PKEY_Media_EncodedBy',
  'PKEY_Media_Writer',
  'PKEY_SoftwareUsed',
  'PKEY_Copyright',
  'PKEY_ParentalRating',
  'PKEY_Image_CompressedBitsPerPixel',
  'PKEY_Media_Publisher',
  'PKEY_Music_Lyrics',
  'PKEY_Media_ContentDistributor',
  'PKEY_Media_ClassPrimaryID',
  'PKEY_ApplicationName',
  'PKEY_ThumbnailStream',
  'PKEY_Media_ClassSecondaryID',
  'PKEY_Music_InitialKey',
  'PKEY_Media_Producer',
  'PKEY_Image_ImageID',
  'PKEY_Music_Genre',
  'PKEY_SimpleRating',
  'PKEY_Media_Year',
  'PKEY_ItemNameDisplay',
  'PKEY_Music_Artist',
  'PKEY_Document_DateSaved',
  'PKEY_Document_LastAuthor',
  'PKEY_Document_Security',
  'PKEY_Document_LineCount',
  'PKEY_Size',
  'PKEY_Document_WordCount',
  'PKEY_Music_BeatsPerMinute',
  'PKEY_FileDescription',
  'PKEY_Media_DateReleased',
  'PKEY_Music_Mood',
  'PKEY_Media_ProviderStyle',
  'PKEY_Language',
  'PKEY_Media_UniqueFileIdentifier',
  'PKEY_Media_ProviderRating',
  'PKEY_Media_MetadataContentProvider',
  'PKEY_Document_Template',
  "PKEY_Music_Conductor",
  "PKEY_Music_Period"
])
editable_keys = set([])

def set_file_details(file_path, file_name):
    try:
        properties = propsys.SHGetPropertyStoreFromParsingName(
            file_path,
            None,
            shellcon.GPS_READWRITE,
            propsys.IID_IPropertyStore
        )
    except Exception as e:
        print(f"Get properties failed for {file_path}.")
        raise

    changed = False
    index = 0
    count = properties.GetCount()
    while index < count:
        property_key = properties.GetAt(index)
        index += 1
        key_name = BuildPKeyToNameMapping().get(property_key, str(property_key))
        property_value = properties.GetValue(property_key).GetValue()
        if ("PKEY" in key_name) and not ("_Photo_" in key_name) and not ("_GPS_" in key_name) and not ("Media_DateEncoded" in key_name) and not ("_DateAcquired" in key_name) and not ("_DateCreated" in key_name):
            # print(f'\t{file_name} => {key_name} => "{property_value}"')
            empty = properties.GetValue(getattr(pscon, key_name)).__class__("")
            value = properties.GetValue(getattr(pscon, key_name)).GetValue()

            try:
                properties.SetValue(getattr(pscon, key_name), empty)
                print(f"{file_name}'s {key_name}: {value}")

                index -= 1
                count -= 1
                changed = True

                editable_keys.add(key_name)
            except:
                pass

    if changed:
        properties.Commit()

def BuildPKeyToNameMapping():
  """Returns a dict mapping PKey values (a tuple of an IID and an int) to their
  names."""
  # The pscon module contains a number of well-known PKey values. Scan through
  # the module picking out anything that looks plausibly like a PROPERTYKEY (a
  # tuple of a PyIID and an int), and map it to its name in the module.
  return {item: name for (name, item) in pscon.__dict__.items() if (
            isinstance(item, tuple) and
            len(item) == 2 and
            isinstance(item[1], int))}

def edit_details_in_folder(folder_paths):
    for folder_path in folder_paths:
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # print(file_path, end='\r')

                try:
                    set_file_details(file_path, file_name)
                except Exception as e:
                    pass

    for val in editable_keys:
        if not val in editable_keynames:
            print(val)

if __name__ == "__main__":
    folder_paths = set([
        r"D:\NAS-01-D\Media",
        # r"E:\NAS-01-E",
        # r"F:\NAS-01-F",
        # r"U:\NAS-01-U\[porn]",
        # r"U:\NAS-01-U\GirlsSection",
        # r"U:\NAS-01-U\impulse"
    ])

    edit_details_in_folder(folder_paths)
