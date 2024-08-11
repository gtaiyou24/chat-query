import {create} from "zustand";
import {persist} from "zustand/middleware";
import {STORAGES} from "@/lib/constants";


type ProjectStore = {
    tenantId: string | null;
    projectId: string | null;
    setTenantId: (newTenantId: string) => void;
    setProjectId: (newProjectId: string) => void;
    reset: () => void;
};


export const useCurrentProjectStore = create<ProjectStore>()(
    persist(
        (set, get) => ({
            tenantId: null,
            projectId: null,
            setTenantId: (newTenantId) => set({
                tenantId: newTenantId,
                projectId: get().tenantId == newTenantId ? get().projectId : null,  // テナントが変更された場合は、プロジェクトを未選択にする
            }),
            setProjectId: (newProjectId) => set({ tenantId: get().tenantId, projectId: newProjectId }),
            reset: () => set({ tenantId: null, projectId: null }),
        }),
        {
            name: STORAGES.project
        }
    )
);