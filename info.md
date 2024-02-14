# Biometrico 

## Install
```
npm i capacitor-native-biometric
npm i bcrypt (opcional)
```
To use android's BiometricPrompt api you must add the following permission to your AndroidManifest.xml:

```
<uses-permission android:name="android.permission.USE_BIOMETRIC">
```

This value is just the reason for using FaceID. You can add something like the following example to App/info.plist:
```
<key>NSFaceIDUsageDescription</key>
<string>Para un inicio de sesión más fácil y rápido.</string>
```

## Biometrico | biometrico.tsx
```
import React, {useEffect, useState} from "react";
import {BiometryType, NativeBiometric} from "capacitor-native-biometric";
import {Preferences} from "@capacitor/preferences";
import {userServices} from "../services/user/user";
import {useAppDispatch} from "../store/hooks";

export const useBiometrico = ({switcher, renderLogin, setErrorMessage}) => {

    const {userLogin} = userServices();
    const dispatch = useAppDispatch();

    const [isBiometricoAvailability, setIsBiometricoAvailability] = useState(false);
    const [isFaceId, setIsFaceId] = useState(false);
    const [isFingerprint, setIsFingerprint] = useState(false);

    useEffect(() => {
        IsUserAndPassword().then(r => {
                if (r) {
                    console.log('user and password exists')
                }
            }
        );

        checkBiometricAvailability().then((r) => {
            setIsBiometricoAvailability(r);
        });

    }, []);

    const checkBiometricAvailability = async () => {
        const resultado = await NativeBiometric.isAvailable();
        if (resultado.isAvailable) {
            setIsFaceId(resultado.biometryType === BiometryType.FACE_ID);
            setIsFingerprint(resultado.biometryType === BiometryType.FINGERPRINT);
            return true;
        }
        return false;
    };

    const performBiometricVerification = async () => {
        const resultado = await NativeBiometric.verifyIdentity({
            reason: "Para un inicio de sesión fácil",
            title: "Iniciar Sesión",
            subtitle: "Usa Huella Digital o Face ID para continuar",
            description: "Escoge tu método de autenticación preferido",
        }).then(() => true)
            .catch(() => false);
        if (resultado) {
            await checkUserAndPassword();
            return resultado;
        }

        return resultado;
    };

    const IsUserAndPassword = async () => {
        const {username, password} = await getUserAndPassword();
        return !(!username || !password);
    }


    const checkUserAndPassword = async () => {
        const {username, password} = await getUserAndPassword();
    }

    const getUserAndPassword = async () => {
        const username = await Preferences.get({key: "username"});
        const password = await Preferences.get({key: "password"});
        return {username: username.value, password: password.value};
    };


    return {
        isBiometricoAvailability,
        performBiometricVerification,
        getUserAndPassword
    };
}
```


## Login Form
```
 import {useAppDispatch} from "../../store/hooks";
import {useEffect, useRef, useState} from "react";
import {
    IonButton,
    IonButtons,
    IonIcon,
    IonInput,
    IonItem,
    IonList,
    IonText,
} from "@ionic/react";
import {ErrorMessage} from "@hookform/error-message";
import {
    arrowForwardCircleOutline,
    eyeOffOutline,
    eyeOffSharp,
    eyeOutline,
    eyeSharp, fingerPrint,
} from "ionicons/icons";
import {addServer} from "../../store/slices/servidorSlice";
import {LoginUrbProps, UserForm} from "../../interfaces/interfaces";
import {addUser} from "../../store/slices/authSlice";
import {userServices} from "../../services/user/user";
import {useForm} from "react-hook-form";
import {useBiometrico} from "../../global-functions/biometrico";
import {Preferences} from "@capacitor/preferences";

const LoginForm: React.FC<LoginUrbProps> = ({
                                                servidor,
                                                setServidor,
                                                errorMessage,
                                                setErrorMessage,
                                                setModalServer,
                                                setResultServidores,
                                                renderLogin,
                                                switcher,
                                            }) => {

    const [isDataAutenticado, setDataAutenticado] = useState(false);
    const [passwordType, setPasswordType] = useState<boolean>(false);
    const dispatch = useAppDispatch();
    const {userLogin, gsServicesAxios} = userServices();
    const [mensaje, setMensaje] = useState("");
    const [mensaje2, setMensaje2] = useState("");

    const {
        handleSubmit,
        register,
        setValue,
        formState: {errors},
    } = useForm<UserForm>();

    useEffect(() => {
        getUserAndPassword().then((r) => {
            // Verificar si username y password no son null ni una cadena vacía
            if (r.username != null && r.username != "" && r.password != null && r.password != "") {
                setMensaje(`Datos: ${r.username} - ${r.password}` );
                setDataAutenticado(true);
            } else{
                setMensaje(`No hay datos: ${r.username} - ${r.password}`);
            }
        });
    }, []);


    const processUserResult = (result,switcher) => {
        if (result.length == 1) {
            setDataAutenticado(true);
            let serv = result[0].servidor;
            let user = result[0].data_user;
            let new_servidor = {
                id: serv.id,
                name: serv.name,
                host: serv.host,
                puerto: serv.puerto,
                url_servicio: serv.url_servicio,
                type: serv.type,
                test: "sss",
            };
            let newUser = {
                userId: user.user_id,
                partnerId: user.partner_id,
                name: user.name,
                vat: user.vat,
                telefono: user.telefono,
                correo: Object.keys(user).includes("correo")
                    ? user.correo
                    : undefined,
                rol: user.rol,
                rolPersona: user.rol_persona,
                image_1920: user.image_1920,
                isLogin: user.isLogin,
                rol_autorizacion: user.rol_autorizacion,
                permission: user.permission,
                session_token: undefined,
                first_login: false,
            };
            setServidor(new_servidor);
            dispatch(addServer(new_servidor));
            dispatch(addUser(newUser));
            setModalServer(false);
            renderLogin();
        } else if (result.length > 1) {
            setResultServidores(result);
            setModalServer(true);
        } else {
            setErrorMessage(
                "No cuenta con opciones de empresas/urbanizaciones asociadas al usuario."
            );
        }
    };

    const {
        isBiometricoAvailability,
        performBiometricVerification,
        getUserAndPassword
    } = useBiometrico({switcher, renderLogin, setErrorMessage});

    const onSubmit = async (formData: UserForm) => {
        setModalServer(false);
        let {status, statusText, data} = await gsServicesAxios(
            JSON.stringify(formData)
        );
        if (status == 200) {
            //guardar en cache username and password
            await Preferences.set({
                key: "username",
                value: formData.username,
            });

            await Preferences.set({
                key: "password",
                value: formData.password,
            });
            if (!Object.keys(data.result).includes("error")) {
                const result = data.result;
                console.log("Response SERVER: ", JSON.stringify(result));
                if (result.length != 0) {
                    processUserResult(result, switcher);
                    if (result.length > 1) {
                        setResultServidores(result);
                        setModalServer(true);
                    }
                } else {
                    setErrorMessage(
                        "No cuenta con opciones de empresas/urbanizaciones asociadas al usuario."
                    );
                }
            } else {
                setErrorMessage(data.result.error);
            }
        } else {
            setErrorMessage(
                `Algo ha salido mal! Intente nuevamente más tarde. De ser posible, comunique este error al departamento de sistemas de Grupo Scanner Express. ${statusText}.`
            );
        }
    };
    const onSumitBiometrico = async () => {
        try {
            const isBiometricVerification = await performBiometricVerification();
            if (isBiometricVerification) {
                setMensaje2("¡Autenticación biométrica exitosa!");
                const {username, password} = await getUserAndPassword();
                setMensaje(`Datos regresando: ${username} - ${password}`);
                const formData = {username: username, password: password};
                const {status, statusText, data} = await gsServicesAxios(
                    JSON.stringify(formData)
                );
                setMensaje(`Datos regresando2: ${status} - ${statusText}`);
                if (status == 200) {
                    setMensaje2(`Sin data: ${data.result} - v,: ${data.result.error} - ${data.result}`);
                    if (!Object.keys(data.result).includes("error")) {
                        const result = data.result;
                        console.log("Response SERVER: ", JSON.stringify(result));
                        setMensaje2("¡Autenticación biométrica exitosa! posiblemten")
                        if (result.length != 0) {
                            processUserResult(result, switcher);
                            if (result.length > 1) {
                                setResultServidores(result);
                                setModalServer(true);
                            }
                        } else {
                            setMensaje2("¡La autenticación biométrica falló!");

                            setErrorMessage(
                                "No cuenta con opciones de empresas/urbanizaciones asociadas al usuario."
                            );
                        }
                    } else {
                        setMensaje2("¡La autenticación biométrica falló!");

                        setErrorMessage(data.result.error);
                    }
                } else {
                    setMensaje2("¡La autenticación biométrica falló!");
                    setErrorMessage(
                        `Algo ha salido mal! Intente nuevamente más tarde. De ser posible, comunique este error al departamento de sistemas de Grupo Scanner Express. ${statusText}.`
                    );
                }
            }else {
                setMensaje2("¡La autenticación biométrica falló!");
            }
        } catch (error) {
        }
    };

    const onkeydown = (ev: any) => {
        if (ev.key === "Enter") {
            setValue("password", ev.target.value);
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit(onSubmit)}>
                <IonList className="flex flex-col">
                    <IonItem lines="full">
                        <IonInput
                            {...register("username", {
                                required: "Este es un campo requerido",
                            })}
                            readonly={servidor ? false : true}
                            label="Usuario"
                            labelPlacement="floating"
                            type="text"
                        />
                    </IonItem>
                    <div className="ion-text-center">
                        <ErrorMessage
                            errors={errors}
                            name="username"
                            as={<div style={{color: "red"}}/>}
                        />
                    </div>
                    <IonItem lines="full">
                        <IonInput
                            {...register("password", {
                                required: "Este es un campo requerido",
                            })}
                            readonly={servidor ? false : true}
                            label="Contraseña"
                            labelPlacement="floating"
                            type={passwordType ? "text" : "password"}
                            onKeyDown={(ev) => onkeydown(ev)}
                        />
                        <IonButtons slot="end">
                            <IonButton onClick={() => setPasswordType(!passwordType)}>
                                <IonIcon
                                    ios={passwordType ? eyeOffOutline : eyeOutline}
                                    md={passwordType ? eyeOffSharp : eyeSharp}
                                />
                            </IonButton>
                        </IonButtons>
                    </IonItem>
                    <div className="ion-text-center">
                        <ErrorMessage
                            errors={errors}
                            name="password"
                            as={<div style={{color: "red"}}/>}
                        />
                    </div>
                </IonList>
                <div className="ion-text-center">
                    <IonButton type="submit" className="flex flex-col my-1 login">
                        Iniciar Sesión
                        <IonIcon slot="end" icon={arrowForwardCircleOutline}/>
                    </IonButton>
                    {(isDataAutenticado && isBiometricoAvailability) && (<div>
                        <div className="container">
                            <div className="line"></div>
                            <div className="text">o ingresar con</div>
                            <div className="line"></div>
                        </div>
                        <IonButton
                            onClick={onSumitBiometrico}
                            className="flex flex-col my-1 login"
                        >
                            Huella / Face ID
                            {/*Icono de huella digital*/}
                            <IonIcon slot="end" icon={fingerPrint}/>
                        </IonButton>
                    </div>)}
                </div>
            </form>
        </>
    );
};

export default LoginForm;

```
