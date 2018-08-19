#!/bin/bash
# Извлекает из файла $NW указанный чанк,
# записывает его в указанную директорию (если чанк изменился)
# подготавливавает сопутствующие файлы 
# формат вызова
# LNW_notangle.sh [-p] [-x] [-r] ROOT_CHANK OUTPUT_DIR
# LNW_notangle.sh [-p] [-x] [-r] ROOT_CHANK -o OUTPUT_FILE
# -x - сделать файл исполнимым
# -p - вывести имя конечного файла на стандартный вывод
# -r - имя файла (или директории) является относительным от директории $PROJ_DIR

# Проверка переменных окружения
if [ -z "$NW" ] ; then
   echo "env var NW is not set. exit from LNW_notangle.sh" 1>&2
   exit 1
fi

if [ ! -f "$NW" ] ; then
    echo "file $NW is not exist. exit from LNW_notangle.sh" 1>&2
    exit 1
fi

if [ -z "$PROJ_DIR" ] ; then
   echo "env var PROJ_DIR is not set. exit from LNW_notangle.sh" 1>&2
   exit 1
fi


# Разбор параметров
PRINT=0
if [ $1 = "-p" ] ; then
   PRINT=1
   shift
fi

EXE=0
if [ $1 = "-x" ] ; then
   EXE=1
   shift
fi

PATH_FROM=""
if [ $1 = "-r" ] ; then
   PATH_FROM="$PROJ_DIR/"
   shift
fi


ROOT=$1
FNAME=$ROOT

if [ "$2" = "-o" ] ; then
   FFNAME="$3"
else 
   if [ -z "$2" ] ; then
       FFNAME="${FNAME}"
   else 
       FFNAME="$2/${FNAME}"
   fi
fi

if [ "${FFNAME:0:1}" != '/' ] ; then
   FFNAME="${PATH_FROM}${FFNAME}"
fi

OUT_DIR=`dirname "$FFNAME"`
OUT_FNAME=`basename "$FFNAME"`

#echo OUT_DIR=$OUT_DIR OUT_FNAME=$OUT_FNAME

mkdir -p "$OUT_DIR/"
FFNAME="${OUT_DIR}/${OUT_FNAME}"
INDEX_FFNAME="${OUT_DIR}/.${OUT_FNAME}.source_nwindex"
INDEX_FFNAME2="${OUT_DIR}/.${OUT_FNAME}.nwindex"


# rm "$FFNAME" "${INDEX_FFNAME}"

T=`mktemp -d`

L=-L'NWHEADSTART line %L file "%F" NWHEADEND'
notangle       -R"$ROOT" "${NW}" >"$T/$FNAME"
notangle "$L"  -R"$ROOT" "${NW}" > "$T/$FNAME".source_nwindex

F=${OUT_DIR}/${OUT_FNAME}.foreign_err

cat "$T/$FNAME" | awk "/\\foreignlanguage/{ print NR - 1; }" >"$F"
if [ -s "$F" ] ; then
    for NR in `cat $F` ; do
        echo "$OUT_DIR/$OUT_FNAME:$NR:0: foreignlanguage LaTeX directive in program text" 1>&2
    done;
#   rm -fr "$T"
#   exit 1
fi
rm $F


LNW_prepare_full_notanle.py "$T/$FNAME" "$T/$FNAME".source_nwindex 1>"$T/$FNAME".source_nwindex_full 2>"$T/$FNAME".source_nwindex_full_err

if [ ! -f "$T/$FNAME".source_nwindex_full ] ; then
   echo Error in LNW_prepare_full_notanle.py "$T/$FNAME" "$T/$FNAME".source_nwindex 1>&2
   cat "$T/$FNAME".source_nwindex_full_err >&2
   exit 1
fi

mv "$T/$FNAME".source_nwindex_full "$T/$FNAME".source_nwindex
cat "$T/$FNAME".source_nwindex | LNW_make_nwindex.py  >"$T/$FNAME".nwindex

cat "$T/$FNAME" | cpif  "$OUT_DIR/$OUT_FNAME"
chmod u+r,g+r,o+r "$OUT_DIR/$OUT_FNAME"

cat "$T/$FNAME".source_nwindex | cpif  "${INDEX_FFNAME}"

cat "$T/$FNAME".nwindex        | cpif "${INDEX_FFNAME2}"


if [ $EXE = 1 ] ; then
  if [ ! -x "$FFNAME" ] ; then 
    chmod +x "$FFNAME"
  fi
fi

if [ $PRINT = 1 ] ; then
   echo "$FFNAME"
fi

rm -fr "$T"

exit 0
