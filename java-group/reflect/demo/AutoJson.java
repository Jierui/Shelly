package com.ndmicro.testhello;

import java.lang.reflect.AccessibleObject;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class AutoJson {
    public static <T> T class2Json(Class<T> c) throws Exception{
        if (c == null) {
            return null;
        }
//        Constructor con = c.getConstructors()[0];
//        Class[] classes = con.getParameterTypes();
//        for (Class cla : classes){
//            cla.newInstance()
//        }
//        con.newInstance();

        T t = c.newInstance();
        List<Field> fieldList = new ArrayList<>() ;
        Class tempClass = c;
        while (tempClass != null) {
        	Field[] fields = tempClass.getDeclaredFields();
            fieldList.addAll(Arrays.asList(tempClass.getDeclaredFields()));
            tempClass = tempClass.getSuperclass(); //得到父类,然后赋给自己
        }
        //Field[] fields = c.getDeclaredFields();
        AccessibleObject.setAccessible(fieldList.toArray(new Field[0]),true);
        for (Field field : fieldList) {
        	if (Modifier.isStatic(field.getModifiers())) {
        		System.out.println("static field:" + field.getName());
        		continue;
        	}
            Class type = field.getType();
            if (type == String.class){
                field.set(t, "default");
            } else if (type == long.class || type == int.class) {
            	field.set(t, 2);
            } else if (Number.class.isAssignableFrom(type)){
                System.out.println("Field:" + field.getName() + type.getName());
                field.set(t,type.getConstructor(String.class).newInstance("1"));
            } else if (type == Date.class){
                System.out.println("Field:" + field.getName() + " is Date");
                field.set(t, new Date());
            }else if (type.isEnum()){
                System.out.println("Field:" + field.getName() + " is Enum");
                Object[] objects = type.getEnumConstants();
                //System.out.println(objects[0].getClass().getName());
                field.set(t, objects[0]);
            }else if (List.class.isAssignableFrom(type)){
                System.out.println("Field:" + field.getName() + " is List");
                Type genericFieldType = field.getGenericType();
                if (genericFieldType instanceof ParameterizedType){
                    ParameterizedType parameterizedType = (ParameterizedType)genericFieldType;
                    Type[] fieldArgTypes = parameterizedType.getActualTypeArguments();
//                    for (Type fileArgType : fieldArgTypes){
//                        Class fieldArgClass = (Class) fileArgType;
//                        System.out.println("class is " + fieldArgClass);
//                    }
                    Class fieldArgClass = (Class) fieldArgTypes[0];
                    ArrayList list = new ArrayList();
                    if (fieldArgClass == String.class){
                        list.add(new String(""));
                    }else if (Number.class.isAssignableFrom(fieldArgClass)){
                        list.add(fieldArgClass.getConstructor(String.class).newInstance("1"));
                    }else {
                        list.add(class2Json(fieldArgClass));
                    }
                    field.set(t,list);
                }
            }else if(Map.class.isAssignableFrom(type)){
            	System.out.println("type is Map");
            	
                Type genericFieldType = field.getGenericType();
                if (genericFieldType instanceof ParameterizedType){
                    ParameterizedType parameterizedType = (ParameterizedType)genericFieldType;
                    Type[] fieldArgTypes = parameterizedType.getActualTypeArguments();
                    Class key = (Class) fieldArgTypes[0];
                    Class value = (Class) fieldArgTypes[1];
                    HashMap mp = new HashMap();
                    Object k,v;
                    if (key == String.class){
                        k = new String("key");
                    }else if (Number.class.isAssignableFrom(key)){
                        k = key.getConstructor(String.class).newInstance("1");
                    }else {
                        k = class2Json(key);
                    }
                    
                    if (value == String.class){
                        v = new String("");
                    }else if (Number.class.isAssignableFrom(value)){
                        v = key.getConstructor(String.class).newInstance("1");
                    }else {
                        v = class2Json(key);
                    }
                    mp.put(k, v);
                    field.set(t, mp);
                }
            }else{
                System.out.println("Field:" + field.getName() + "is  object " + field.getType().getName());
                field.set(t, class2Json(type));
            }
        }
        return t;
    }
}
